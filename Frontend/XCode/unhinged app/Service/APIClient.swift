//
//  APIClient.swift
//  unhinged app
//
//  Created by Harry Sho on 11/25/24.
//

import Foundation

class APIClient {
    
    //TODO: create websocket task manager, endpoint: <socket.io/>
    static let shared = APIClient()
    private init() {}
    enum TaskType {
        case get
        case post
    }
    enum TaskError : Error{
        case failedToSaveToken
        case invalidValue(String)
    }

    private func apiTask(type: TaskType, endpoint: String, hasHeader:Bool, headerValue: String?  = "", headerField: String? = "", queryItems: [URLQueryItem]? = nil,  payload: Data?, completion: @escaping (Result<Data, Error>) -> Void) {
        // Construct the URL
        var urlComponents = URLComponents(string: "https://cowbird-expert-exactly.ngrok-free.app/\(endpoint)")!
        urlComponents.queryItems = queryItems ?? []
        guard let url = urlComponents.url else {
            completion(.failure(NSError(domain: "Invalid URL", code: 0, userInfo: nil)))
            return
        }

        // Create the request
        var request = URLRequest(url: url)
        request.httpMethod = type == .get ? "GET" : "POST"
        if (hasHeader){
            request.setValue(headerValue ?? "", forHTTPHeaderField: headerField ?? "")
        }
        
        // Set headers and body for POST requests
        if type == .post {
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            request.httpBody = payload
        }

        // Create the data task
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            // Handle errors
            if let error = error {
                completion(.failure(error))
                return
            }

            // Check for a valid HTTP response
            guard let httpResponse = response as? HTTPURLResponse else {
                completion(.failure(NSError(domain: "Invalid Response", code: 0, userInfo: nil)))
                return
            }
            print("Response String: \(httpResponse)")

            // Check for a successful status code (e.g., 200-299)
            guard (200...299).contains(httpResponse.statusCode) else {
                completion(.failure(NSError(domain: "Server Error", code: httpResponse.statusCode, userInfo: nil)))
                return
            }

            // Handle the response data
            if let data = data {
                completion(.success(data))
            } else {
                completion(.failure(NSError(domain: "No Data", code: 0, userInfo: nil)))
            }
        }

        // Start the task
        task.resume()
    }
    
    //send identity token
    struct IdentityTokenResponse : Codable {
        let message : String
        let token : String
    }
    func sendIdentityToken(token: String) {
        print("Sending identity token")
        let body : [String : String] = ["auth_method": "apple",
                                        "identity_token": token]
        guard let payload = try? JSONEncoder().encode(body) else {
            print("failed to encode payload")
            return
        }
        apiTask(type: .post, endpoint: "signup", hasHeader: false, payload: payload){result in
            switch result {
                case .success(let data):
                    do {
                        let tokenResponse : IdentityTokenResponse = try JSONDecoder().decode(IdentityTokenResponse.self, from: data)
                        let success = KeychainHelper.save(key: "JWTToken", value: tokenResponse.token)
                        if success {
                            print("Successfully saved token")
                            try self.verifyJWTToken()
                        } else {
                            print("Failed to save token")
                        }
                        
                    } catch {
                        print("Failed to decode JSON: \(error.localizedDescription)")
                    }
                case .failure(let error):
                    print("Error: \(error.localizedDescription)")
                }
        }
    }
    
    //verify JWT Token
    func verifyJWTToken() throws {
        let token : String = KeychainHelper.load(key: "JWTToken")!
        print(token as String)
        apiTask(type: .get, endpoint: "verify_token", hasHeader: true, headerValue: "Bearer \(token)", headerField: "X-Authorization", payload: nil){result in
            switch result {
            case .success(let data):
                do {
                    let response : [String:String] = try JSONDecoder().decode([String:String].self, from: data)
                    print(response)
                } catch {
                    print("Failed to decode JSON: \(error.localizedDescription)")
                }
                print("Verified Token Success")
            case .failure(let error):
                print("Verify Token Failed: \(error)")
            }
            
        }
    }

    
    //TODO: implement gallery data flow
    //TODO: implement prompts data flow
    //Push Profile
    func initProfile(profile: Profile) {
        let token : String = KeychainHelper.load(key: "JWTToken")!
        let profileData : [String:String] = ["age":"\(profile.age)",
                                             "name":profile.name,
                                             "gender":"\(profile.gender.rawValue)",
                                             "state":"\(profile.state.rawValue)",
                                             "city":profile.city,
                                             "bio":profile.biography]
        guard let payload = try? JSONEncoder().encode(profileData) else {
            fatalError("Failed to encode payload")
        }
        apiTask(type: .post, endpoint: "users/profile", hasHeader: true ,headerValue: "Bearer \(token)", headerField: "X-Authorization", payload: payload){ result in
            switch result {
            case .success(let data):
                do {
                    let response : [String:String] = try JSONDecoder().decode([String:String].self, from: data)
                    print(response)
                } catch {
                    print("Failed to decode JSON: \(error.localizedDescription)")
                }
            case .failure(let error):
                print("Init profile failed: \(error.localizedDescription)")
            }
        }
    }
    
    //Push Preferences
    func pushPreference(preference: MatchPreference){
        print("attempting to push preference")
        let token : String = KeychainHelper.load(key: "JWTToken")!
        let preferenceData : [String:String]  = ["minAge":"\(preference.minAge)",
                                                 "maxAge":"\(preference.maxAge)",
                                                 "interestedIn":"\(preference.interestedIn)"]
        guard let payload = try? JSONEncoder().encode(preferenceData) else {
            fatalError("Failed to encode payload")
        }
        
        let urlQueryItems = [URLQueryItem(name: "limit", value: "20")]
        
        apiTask(type: .post, endpoint: "users/preferences", hasHeader: true ,headerValue: "Bearer \(token)", headerField: "X-Authorization", queryItems: urlQueryItems, payload: payload){result in
            switch result {
            case .success(let data):
                do {
                    let response : [String:String] = try JSONDecoder().decode([String:String].self, from: data)
                    print(response)
                } catch {
                    print("Failed to decode JSON: \(error.localizedDescription)")
                }
            case .failure(let error):
                print("Push Preference failed: \(error.localizedDescription)")
            }
        }
        
    }
    
    //Get Swipe profiles for MatchView()
    func decodeProfile (person: [String:String]) throws -> Profile  {
        guard let idString  = person["userID"] else {
            throw TaskError.invalidValue("idstring")
        }
        let id = Int(idString)
        
        guard let ageString    = person["age"] else {
            throw TaskError.invalidValue("agestring")
        }
        let age: Int    = Int(ageString)!
        
        guard let name   = person["name"] else {
            throw TaskError.invalidValue("nameString")
        }
        
        guard let genderString = person["gender"] else {
            throw TaskError.invalidValue("genderString")
        }
        guard let gender = ProfileGender(rawValue: genderString) else{
            print("Failed to match ProfileGender case: \(genderString)")
            throw TaskError.invalidValue("\(genderString)")
        }
        
        let stateString  = person["state"]
        guard let stateCode = USState(rawValue: stateString ?? "") else {
            print("Failed to match USState case: \(String(describing: stateString))")
            throw TaskError.invalidValue("stateCode")
        }
        
        guard let cityString: String   = person ["city"] else {
            print("invalid city string")
            throw TaskError.invalidValue("cityString")
        }
        guard let bioString: String    = person["bio"] else {
            print("invalid bio string")
            throw TaskError.invalidValue("bioString")
        }
        
        return Profile(id: id!, name: name, age: age , gender: gender, state: stateCode, city: cityString, bio: bioString)
    }
    func getSwipes (limit: Int) -> [Profile] {
        print("Attempting to pull swipe pool")
        let token : String = KeychainHelper.load(key: "JWTToken")!
        var profiles : [Profile] = []
        apiTask(type: .get, endpoint: "/users/swipe_pool", hasHeader: true, headerValue: "Bearer \(token)", headerField: "X-Authorization", payload: nil){ result in
            switch result {
            case .success(let data):
                do {
                    let response : [[String:String]] = try JSONDecoder().decode([[String:String]].self, from: data)
                    print(response)
                    for person in response {
                        try profiles.append(self.decodeProfile(person: person))
                    }
                } catch {
                    print("Failed to decode profile: \(error.localizedDescription)")
                }
                
            case .failure(let error):
                print("getSwipes failed with error: \(error.localizedDescription)")
            }
        }
        
        return profiles
    }
    
    //Get Matches for ConversationsView()
    func getMatches () -> [Conversation] {
        
        var pulledConversations : [Conversation] = []
        let token : String = KeychainHelper.load(key: "JWTToken")!
        
        print("Attempting to pull matches")
        apiTask(type: .get, endpoint: "users/matches", hasHeader: true, headerValue: "Bearer \(token)", headerField: "X-Authorization", payload: nil){ result in
            switch(result){
            case .success(let data):
                do {
                    let response : [[String:String]] = try JSONDecoder().decode([[String:String]].self, from: data)
                    print(response)
                } catch {
                    print("Failed to decode JSON: \(error.localizedDescription)")
                }
                break
            case .failure(let error):
                print("getMatches failed with error: \(error.localizedDescription)")
                break
            }
        }
        
        return pulledConversations
    }
    
    //Get messages associated with a match (Conversation)
    func getConversationMessages (match_id: String, page: Int?, all_messages: Bool?) -> [Message] {
        var pulledMessages : [Message] = []
        
        print("Attmepting to pull messages for match_id: \(match_id)")
        /*
         apiTask(type: .get, endpoint: "users/messages/conversation", hasHeader: <#T##Bool#>, payload: <#T##Data?#>, completion: <#T##(Result<Data, any Error>) -> Void#>){ result in
            switch(result){
            case .success(let data):
             break
            case .failure(let error):
             print("getMatches failed with error: \(error.localizedDescription)")
             break
            }
        }
         */
        
        return pulledMessages
    }
    
    //TODO: additional backend routes
    
    //Send message to conversation associated with match
    func pushConversationMessage (match_id: String, type: Message.Kind?, content: String) {
        
        
    }
    
    func pushSwipe (swiped_user_id: String, accepted: Bool){
        
        
        
    }
    
    /*
     
    func pushProfileItem() -> Bool {
        
        
    }
     
     */
    
    
    
}

