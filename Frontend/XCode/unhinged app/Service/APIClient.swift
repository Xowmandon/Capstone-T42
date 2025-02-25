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
    
    
    private func apiTask(type: TaskType, endpoint: String, payload: Data?, completion: @escaping (Result<Data, Error>) -> Void) -> Bool {
        
        guard let url = URL(string: "https://cowbird-expert-exactly.ngrok-free.app/\(endpoint)") else {
            
            completion(.failure(NSError(domain: "Invalid URL", code: 0, userInfo: nil)))
            
            return false
            
        }
        
        if type == .get {
            APIClient.connection.dataTask(with: url) { data, response, error in
                
                completion(.success(data!))
                
            }
        } else if type == .post {
            
            var request = URLRequest(url: url)
            
            request.httpMethod = "POST"
            request.httpBody = payload
            
            APIClient.connection.uploadTask(with: request, from: payload!).resume()
            
            
            completion(.success(Data()))
            
        }
        
        return true
        
    }
     
     //check if account associated with ID exists
    func assertAccountExistence(userEmailID: String) -> Bool {
        
        print("asserting account existence")
       
        apiTask(type: .get, endpoint: "", payload: nil){ data in
            
            
        
        }
        
        return false
       
    }
    
    func createAccount(account: AccountData) {
        
        struct AccountJSON: Codable {
            let name: String
            let email: String
        }
        
        let accountInfo : AccountJSON = AccountJSON(name: account.getProfile().name, email: account.getEmail()!)
        
        let payload = try! JSONEncoder().encode(accountInfo)
        
        print("pushing JSON payload")
        print(payload)
        
        apiTask(type: .post, endpoint: "users", payload: payload){data in}
        
        
    }
    
    func test_post_user() {
        
        // Define the payload
        let payload: [String: Any] = [
            "email": "HarryPotter@2hogwarts.com",
            "name": "Harry Potter",
            "username": "hp123"
        ]

        // Convert the payload to JSON data
        guard let jsonData = try? JSONSerialization.data(withJSONObject: payload) else {
            print("Error: Unable to encode JSON payload.")
            return
        }

        // Create the URL
        guard let url = URL(string: "https://cowbird-expert-exactly.ngrok-free.app/users") else {
            print("Error: Invalid URL.")
            return
        }

        // Create a URLRequest and set its properties
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData

        // Create a data task to send the request
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error: \(error.localizedDescription)")
                return
            }

            if let response = response as? HTTPURLResponse {
                print("Response Status Code: \(response.statusCode)")
            }

            if let data = data, let responseBody = String(data: data, encoding: .utf8) {
                print("Response Body: \(responseBody)")
            }
        }

        // Start the task
        task.resume()
    }
    
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

