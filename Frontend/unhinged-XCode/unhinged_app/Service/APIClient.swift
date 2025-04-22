//
//  APIClient.swift
//  unhinged app
//
//  Created by Harry Sho on 11/25/24.
//  Pair Programmed With Joshua Ferguson (Xowmandon)
//

import Foundation

class APIClient {
    
    //TODO: create websocket task manager, endpoint: <socket.io/>
    static let shared = APIClient()
    private init() {}
    enum TaskType {
        case get
        case post
        case postForm
    }
    enum TaskError : Error{
        case failedToSaveToken
        case invalidValue(String)
    }
    
    func apiTask(
        type: TaskType,
        endpoint: String,
        hasHeader: Bool,
        headerValue: String? = "",
        headerField: String? = "",
        queryItems: [URLQueryItem]? = nil,
        payload: Data?
    ) async throws -> Data {
        
        var urlComponents = URLComponents(string: "https://cowbird-expert-exactly.ngrok-free.app/\(endpoint)")!
        urlComponents.queryItems = queryItems ?? []
        
        guard let url = urlComponents.url else {
            throw URLError(.badURL)
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = type == .get ? "GET" : "POST"
        
        if hasHeader {
            request.setValue(headerValue ?? "", forHTTPHeaderField: headerField ?? "")
        }
        
        switch type {
        case .post:
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            request.httpBody = payload
        case .postForm:
            request.httpMethod = "POST"
            request.setValue("multipart/form-data", forHTTPHeaderField: "Content-Type")
            request.httpBody = payload
        default:
            break
        }

        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw URLError(.badServerResponse)
        }
        
        return data
    }
    
    /*
    private func apiTask(type: TaskType, endpoint: String, hasHeader:Bool, headerValue: String?  = "", headerField: String? = "", queryItems: [URLQueryItem]? = nil,  payload: Data?, completion: @escaping (Result<Data, Error>) -> Void) async {
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

        else if type == .postForm {
            request.httpMethod = "POST"
            request.setValue("multipart/form-data", forHTTPHeaderField: "Content-Type")
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
    */
    
    //send identity token
    struct IdentityTokenResponse : Codable {
        let message : String
        let token : String
    }
    func sendIdentityToken(token: String) async {
        print("Sending identity token")
        let body : [String : String] = ["auth_method": "apple",
                                        "identity_token": token]
        guard let payload = try? JSONEncoder().encode(body) else {
            print("failed to encode payload")
            return
        }
        do {
            let data = try await apiTask(type: .post, endpoint: "signup", hasHeader: false, payload: payload)
            let tokenResponse : IdentityTokenResponse = try JSONDecoder().decode(IdentityTokenResponse.self, from: data)

            let success = KeychainHelper.save(key: "JWTToken", value: tokenResponse.token)
            if success {
                print("Successfully saved token")
                try await self.verifyJWTToken()
            } else {
                print("Failed to save token")
            }
            
        } catch {
            print("Failed to receive Token: \(error.localizedDescription)")
        }

    }
    
    //verify JWT Token
    func verifyJWTToken() async throws {
        let token : String = KeychainHelper.load(key: "JWTToken")!
        print(token as String)
        do {
            let data = try await apiTask(type: .get, endpoint: "verify_token", hasHeader: true, headerValue: "Bearer \(token)", headerField: "X-Authorization", payload: nil)
            let response : [String:String] = try JSONDecoder().decode([String:String].self, from: data)
            print(response)
        } catch {
            print("Verify Token Failed: \(error)")
        }
        print("Verified Token Success")
    }
    
    
    //TODO: implement gallery data flow
    //TODO: implement prompts data flow
    //Push Profile
    func initProfile(profile: Profile) async {
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
        do {
            let data = try await apiTask(type: .post, endpoint: "users/profile", hasHeader: true ,headerValue: "Bearer \(token)", headerField: "X-Authorization", payload: payload)
            let response : [String:String] = try JSONDecoder().decode([String:String].self, from: data)
            print(response)
        } catch {
            print("Failed to init profile: \(error.localizedDescription)")
        }
        
    }
    
    //Push Preferences
    func pushPreference(preference: MatchPreference) async {
        print("attempting to push preference")
        let token : String = KeychainHelper.load(key: "JWTToken")!
        let preferenceData : [String:String]  = ["minAge":"\(preference.minAge)",
                                                 "maxAge":"\(preference.maxAge)",
                                                 "interestedIn":"\(preference.interestedIn)"]
        guard let payload = try? JSONEncoder().encode(preferenceData) else {
            fatalError("Failed to encode payload")
        }
        
        let urlQueryItems = [URLQueryItem(name: "limit", value: "20")]
        
        do {
            let data = try await apiTask(type: .post, endpoint: "users/preferences", hasHeader: true ,headerValue: "Bearer \(token)", headerField: "X-Authorization", queryItems: urlQueryItems, payload: payload)
            let response : [String:String] = try JSONDecoder().decode([String:String].self, from: data)
            print(response)
        } catch {
            print("Push Preference failed: \(error.localizedDescription)")
        }
        
    }
    
    // MARK: GetSwipes
    //Get Swipe profiles for MatchView()
    func decodeProfile (person: [String:String]) throws -> Profile  {
        guard let idString  = person["userID"] else {
            throw TaskError.invalidValue("idstring")
        }
        
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
        
        return Profile(id: idString, name: name, age: age , gender: gender, state: stateCode, city: cityString, bio: bioString)
    }
    
    func getSwipes (limit: Int) async -> [Profile] {
        print("Attempting to pull swipe pool")
        let queryLimit : [URLQueryItem] = [URLQueryItem(name: "limit", value: String(limit))]
        let token : String = KeychainHelper.load(key: "JWTToken")!
        var profiles : [Profile] = []
        do {
            let data = try await apiTask(type: .get, endpoint: "users/swipe_pool", hasHeader: true, headerValue: "Bearer \(token)", headerField: "X-Authorization", queryItems: queryLimit, payload: nil)
            print(data as Any)
            let response : [[String:String]] = try JSONDecoder().decode([[String:String]].self, from: data)
            print(response)
            for person in response {
                print("decoding \(person)")
                let personProfile = try self.decodeProfile(person: person)
                
                /*
                let decodedName = personProfile.name
                print("decodedName: \(decodedName)")
                let decodedID = personProfile.profile_id
                print("decodedID : \(decodedID)")
                */
                profiles.append(personProfile)
            }
        } catch {
            print("getSwipes failed with error: \(error.localizedDescription)")
        }
        
        print("pulled profiles: \(String(describing: profiles))")
        
        return profiles
    }
    
    //Get Matches for ConversationsView()
    /*
    struct getMatchesResponse : Decodable {
        let id : String
        let matchedUserId : String
        let matchedName : String
        let matchDate : String
        let lastMessage : String
        let profile : [String:String]
    }
     */
    func getMatches () async -> [Conversation] {
        
        var pulledConversations : [Conversation] = []
        let token : String = KeychainHelper.load(key: "JWTToken")!
        
        print("Attempting to pull matches")
        do {
            let data = try await apiTask(type: .get, endpoint: "users/matches", hasHeader: true, headerValue: "Bearer \(token)", headerField: "X-Authorization", payload: nil)
            let response : [[String:String]] = try JSONDecoder().decode([[String:String]].self, from: data)
            print(response)
            for match in response {
                print (match)
                
                guard   let id = match["match_id"],
                        let matchedUserId = match["matched_user_id"],
                        let matchedName = match["matched_user_name"],
                        let matchDate = match["match_date"],
                        let lastMessage = match["last_message"] else {
                    
                    throw NSError(domain: "Failed to decode", code: 1000, userInfo: nil)
                }
                guard let matchedProfile = await getProfile(userID: matchedUserId) else {
                    throw NSError(domain: "No profile exists", code: 1000, userInfo: nil)
                }
                let conversation = Conversation(matchId: id,
                                                matchedUserId: matchedUserId,
                                                matchedName: matchedName,
                                                matchDate: matchDate,
                                                lastMessage: lastMessage,
                                                matchedProfile: matchedProfile)
                
                pulledConversations.append(conversation)
            }
            
        } catch {
            print("getMatches failed with error: \(error.localizedDescription)")
        }
        return pulledConversations
    }
    
    //Get messages associated with a match (Conversation)
    func getConversationMessages (match_id: String,limit: Int?, page: Int?, all_messages: Bool?) async -> [Message] {
        // Author: Joshua Ferguson (Xowmandon)

        var pulledMessages : [Message] = []
        
        
        print("Attmepting to pull messages for match_id: \(match_id)")
        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return pulledMessages
        }
        // URL Parameters
        var queryItems = [ URLQueryItem(name: "match_id", value: match_id) ]
        
        if let limitOpt = limit {
            queryItems.append(URLQueryItem(name: "limit", value: String(limitOpt)))
        }
        if let pageOpt = page {
            queryItems.append(URLQueryItem(name: "page", value: String(pageOpt)))
        }
        
        if let all_messages_opt = all_messages {
            queryItems.append(URLQueryItem(name: "all_messages", value: String(all_messages_opt)))
        }
        
        
        do {
            let data = try await apiTask(
                type: .get,
                endpoint: "users/messages/conversation",
                hasHeader: true,
                headerValue: "Bearer \(token)",
                headerField: "X-Authorization",
                queryItems: queryItems,
                payload: nil
            )
            let decoder = JSONDecoder()
            let resp = try decoder.decode(MessageResponse.self, from: data)
            let messages = resp.messages
            pulledMessages = messages
            print("Total \(messages.count) messages for match \(resp.matchId): Queried So Far \(resp.totalMessages)")
        }
        catch {
            print("⚠️ decode failed:", error)
        }
        return pulledMessages
    }
        //TODO: additional backend routes
        
    //Send message to conversation associated with match
    func pushConversationMessage (match_id: String, type: Message.Kind?, content: String) async {
        // Author: Joshua Ferguson (Xowmandon)

        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return
        }

        var payload: [String: Any] = ["match_id": match_id,
                                      "message_content": content,]
        // if you ever want to send kind to server:
        if let kind = type {
            payload["kind"] = kind.rawValue
        }

        // 3️⃣ Serialize to Data
        guard let body = try? JSONSerialization.data(withJSONObject: payload, options: []) else {
            print("❌ Failed to serialize JSON payload")
            return
        }

        do {
            let data = try await apiTask(
                type: .post,
                endpoint: "users/messages",
                hasHeader: true,
                headerValue: "Bearer \(token)",
                headerField: "X-Authorization",
                queryItems: nil,
                payload: body
            )
            print("✅ Message sent successfully")
        } catch {
            print("❌ pushConversationMessage failed:", error.localizedDescription)
        }
    }
        
    func pushSwipe(swipedUserId: String, accepted: Bool) async -> String? {
        // Author: Joshua Ferguson (Xowmandon)

        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return nil
        }
        
        let result: SwipeResult = accepted ? SwipeResult.pending : SwipeResult.rejected
        let swipe = Swipe(
            swiperId:    nil,
            swipeeId:    swipedUserId,
            swipeResult: result,
        )
        
        let encoder = JSONEncoder()
        let decoder = JSONDecoder()
        
        // Make POST Request, with JWT TOken
        do {
            let body = try encoder.encode(swipe)
            let data = try await apiTask(
                type: TaskType.post,
                endpoint: "users/swipes",
                hasHeader: true,
                headerValue: "Bearer \(token)",
                headerField: "X-Authorization",
                payload: body
            )
            
            do {
                // Check for New Match Object
                let resp = try decoder.decode(SwipeResponse.self, from: data)
                //print("✅ \(resp["status"])")
                if let matchId = resp.matchId {
                    // 🎉 New match! handle it here
                    print("🎉 New match detected! match_id = \(matchId)")
                    return resp.status
                    // e.g. navigate to chat screen, notify UI, etc.
                } else {
                    // ✅ Swipe went through, but no match yet
                    print("✅ Swipe sent successfully. No match detected.")
                }
                
            } catch {
                print("⚠️ Could not parse response:", error)
            }
        } catch {
            print("❌ failed to encode Swipe payload:", error)
        }
        
        return ""
    }
    
    func pollMatches() async {
        // Author: Joshua Ferguson (Xowmandon)
        
        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return
        }

        // Poll for new matches
        // Make GET Request, with JWT Token
        let decoder = JSONDecoder()
        do {
            let data = try await apiTask(
                type: .get,
                endpoint: "poll/matches",
                hasHeader: true,
                headerValue: "Bearer \(token)",
                headerField: "X-Authorization",
                queryItems: nil,
                payload: nil
            )
    
            let resp = try decoder.decode(PollMatchesResponse.self, from: data)
            if resp.status == "NEW" {
                print("🎉 New match detected!")
                
                // Handle new match here (TODO)
                // Resp Structure:
                // {
                //     "status": "NEW",
                //     "match_id": "12345",
                //     "matched_user_id": "67890",
                //     "matched_user_name": "John Doe",
                //     "match_date": "2023-10-01T12:00:00Z",
                //     "last_message": "Hello!"
                // }
                
            } else {
                print("No new matches.")
            }
        } catch {
            print("⚠️ Could not parse response:", error.localizedDescription)
        }
        // Send Signal if Returns New Match
        
    }
    
    func pollMessages(matchId: String? = nil) async {
        // Author: Joshua Ferguson (Xowmandon)

        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return
        }

        print("Attempting to poll messages...Match ID: \(matchId ?? "No Match ID")")

        // If matchId is nil, then poll all messages
        // If matchId is not nil, then poll messages for that matchId
        let queryItems = matchId != nil ? [URLQueryItem(name: "match_id", value: matchId)] : nil

        let decoder = JSONDecoder()
        do {
            let data = try await apiTask(
                type: .get,
                endpoint: "poll/messages",
                hasHeader: true,
                headerValue: "Bearer \(token)",
                headerField: "X-Authorization",
                queryItems: queryItems,
                payload: nil
            )
            let resp = try decoder.decode(PollMessagesResponse.self, from: data)
            if resp.status == "NEW" {
                
                // Sanity & Validation Print
                print("🎉 New messages detected for match_id: \(resp.matchId ?? "")")
                print("Messages: \(resp.messages)")
                print("Total messages: \(resp.messages.count)")
                
                
                // Handle new messages here (TODO)
                // Resp Structure:
                // {
                //     "status": "NEW",
                //     "match_id": "12345",
                //     "messages": [
                //         {
                //             "message_id": "1",
                //             "content": "Hello!",
                //             "sentFromClient": true,
                //             ...
                //         },
                //         ...
                //     ]
                // }
                
            } else {
                print("No new messages Found.")
            }
        } catch {
            print("⚠️ Could not parse response:", error.localizedDescription)
        }
    }
    
    
    // MARK: Get profile
    func getProfile(userID: String) async -> Profile? {
        var profile: Profile?
        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return nil
        }

        let queryItems = [URLQueryItem(name: "user_id", value: userID)]
        
        do {
            let data = try await apiTask(type: .get,
                                         endpoint: "users/profile",
                                         hasHeader: true,
                                         headerValue: "Bearer \(token)",
                                         headerField: "X-Authorization",
                                         queryItems: queryItems,
                                         payload: nil)
            let response : [String:String] = try JSONDecoder().decode([String:String].self, from: data)
            print(response)
            profile = try decodeProfile(person: response)
            
        } catch {
            print("Get Profile failed with error \(error.localizedDescription)")
        }
        return profile
    }
    
    
/*
    func postProfileImg(mainPhoto: Bool =  false, image: UIImage ) {
     // Author: Joshua Ferguson (Xowmandon)
    //Post profile image to server, mainPhoto is defaulted to false
        //var endpoint = "users/profile_picture"
        //var contentType = "multipart/form-data"

        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return
        }

        print("Attempting to post profile image...")

        // Salt for FileName, Str of Length 8?
        var fileNameSalt = NSUUID().uuidString
        print("FileName Salt: \(fileNameSalt)")

        // COnstruct Form Data
        let multipartFormData = MultipartFormData()

        // Append the image data
        // Convert UIImage to JPEG data
        // Append the image data to the multipart form data
        multipartFormData.append(
            image.jpegData(compressionQuality: 0.8)!,
            withName: "profile_picture",
            fileName: "\(fileNameSalt).jpg",
            mimeType: "image/jpeg"
        )

        //Append is_main_photo Bool to Form Data
        multipartFormData.append(
            Data("\(mainPhoto)".utf8), // Convert Bool to String
            withName: "is_main_photo"
        )

        // COnstruct Request
        apiTask(
            type: .postForm,
            endpoint:  "users/profile_picture",
            hasHeader: true,
            headerValue: "Bearer \(token)",
            headerField: "X-Authorization",
            queryItems: nil,
            payload: multipartFormData.data
        ) { result in
            switch result {
            case .success:
                print("✅ Profile image posted successfully")
                // Py - return jsonify({"success": "Profile Uploaded", "url": url}), 201

                // Decode Response
                let decoder = JSONDecoder()
                do {
                    let resp = try decoder.decode([String: String].self, from: data)
                    print("postProfileImg Response: \(resp)")
                    
                    let imgURL = resp["url"] // S3 URL
                    print("Image URL: \(imgURL ?? "No URL")")

                } catch {
                    print("⚠️ Could not parse response:", error)
                }


            case .failure(let error):
                print("❌ postProfileImg failed:", error.localizedDescription)
            }
        }


    }
    func getProfileImgs(userId: String? = nil) {
        // Author: Joshua Ferguson (Xowmandon)

        // Get profile images from server
        // Make GET Request, with JWT Token
        guard let token = KeychainHelper.load(key: "JWTToken") else {
            print("❌ No JWT token found")
            return
        }

        print("Attempting to get profile images...")

        // If userId is nil, then get ProfileImg for Current User
        // else get ProfileImg for that userId
        let queryItems = (userId != nil) ? [URLQueryItem(name: "user_id", value: userID)] : nil

        // Construct Request for Profile Imgs of UserID
        apiTask(
            type: .get,
            endpoint: "users/profile_picture",
            hasHeader: true,
            headerValue: "Bearer \(token)",
            headerField: "X-Authorization",
            queryItems: queryItems,
            payload: nil
        ) { result in
            switch result {
            case .success:
                print("✅ getProfileImgs Success")
                // Decode Response
                let decoder = JSONDecoder()
                do {
                    // Decode the Python response S3 URLS
                    let resp = try decoder.decode([String: [String]].self, from: data)
                    mainPhoto = resp["main_photo"] // S3 URL
                    additionalPhotos = resp["user_photos"] // S3 URL
                    
                    // Validation Print
                    print("Main Photo URL: \(mainPhoto ?? "No URL")")
                    print("Additional Photos URLs: \(additionalPhotos ?? ["No URL"])")
                    
                } catch {
                    print("⚠️ Could not parse response:", error)
                }
            case .failure(let error):
                print("❌ getProfileImgs failed:", error.localizedDescription)
            }
        }
        
    }
    */
    
    /*
     
     func pushProfileItem() -> Bool {
     
     
     }
     
     */
    
    
    
}


struct PollMatchesResponse: Codable {
let status: String
let matchId: String?
let matchedUserId: String?
let matchedUserName: String?
let matchDate: String?
let lastMessage: String?

enum CodingKeys: String, CodingKey {
    case status
    case matchId = "match_id"
    case matchedUserId = "matched_user_id"
    case matchedUserName = "matched_user_name"
    case matchDate = "match_date"
    case lastMessage = "last_message"
}

}


struct PollMessagesResponse: Codable {
let status: String
let matchId: String?
let messages: [Message]

enum CodingKeys: String, CodingKey {
    case status = "status"
    case matchId = "match_id"
    case messages = "messages"
}
}
