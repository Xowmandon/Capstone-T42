//
//  APIClient.swift
//  unhinged app
//
//  Created by Harry Sho on 11/25/24.
//

import Foundation

class APIClient {
    
    //establish connection with database
    static let shared = APIClient()
    private static let connection : URLSession = URLSession.shared //URLSession(configuration: URLSessionConfiguration.default)
    
    private init() {
        
        /*
        connectWithAPI(endpoint: "http//unhinged-api.com"){result in
            
            switch result {
            case .success(let data):
                break
            case .failure(let error):
                print(error)
                break
            }
            
        }
         */
     
    }
    enum TaskType {
        case get
        case post
    }

    private func apiTask(type: TaskType, endpoint: String, payload: Data?, completion: @escaping (Result<Data, Error>) -> Void) {
        // Construct the URL
        guard let url = URL(string: "https://cowbird-expert-exactly.ngrok-free.app/\(endpoint)") else {
            completion(.failure(NSError(domain: "Invalid URL", code: 0, userInfo: nil)))
            return
        }

        // Create the request
        var request = URLRequest(url: url)
        request.httpMethod = type == .get ? "GET" : "POST"
        
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
    
    func sendIdentityToken(token: String) {
        print("Sending identity token")
        let body : [String : String] = ["auth_method": "apple",
                    "identity_token": token]
        guard let payload = try? JSONEncoder().encode(body) else {
            print("failed to encode payload")
            return
        }
        
        apiTask(type: .post, endpoint: "signup", payload: payload){result in
            switch result {
                case .success(let data):
                    do {
                        let dataString = try JSONDecoder().decode(String.self, from: data)
                        
                        
                    } catch {
                        print("Failed to decode JSON: \(error.localizedDescription)")
                    }
                case .failure(let error):
                    print("Error: \(error.localizedDescription)")
                }
        }
    }
     
     //check if account associated with ID exists
    func assertAccountExistence(userEmailID: String) -> Bool {
        print("asserting account existence")
        apiTask(type: .get, endpoint: "", payload: nil){ data in
            
        }
        return false
    }
    
    /*
    func createAccount(account: AccountData) {
        struct AccountJSON: Codable {
            let name: String
            let email: String
        }
        let accountInfo : AccountJSON = AccountJSON(name: account.getProfile().name, email: account.getEmail()!)
        let payload = try! JSONEncoder().encode(accountInfo)
        print("pushing JSON payload")
        print(payload)
        apiTask(type: .post, endpoint: "users", payload: payload){data in
            
        }
    }
    */
    
    /*
    // Get list of possible profiles to match
    func getProspects() -> [Profile] {
        
        
        
    }
     
    
    // Like a profile
    func createMatch() {
        
        //api.add to liked list
        
    }
    
    // Reject a profile
    func rejectMatch() {
        
        //api.add to dislike list
        
    }
     
    func getConversations(forProfile: ProfileID) -> [Conversation] {
        
        
        
    }
     
    func getMessages(withConversationID: ConversationID) -> EC2Response {
        
        
        
    }
     
    func pushMessage() -> EC2Response {
        
        
        
    }
     
    func pushProfileItem() -> Bool {
        
        
    }
     
     */
    
    
    
}

