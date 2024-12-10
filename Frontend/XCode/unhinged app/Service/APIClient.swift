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
    private static let connection : URLSession = URLSession(configuration: URLSessionConfiguration.default)
    
    private init() {
     
        connectWithAPI(endpoint: "http//unhinged-api.com"){result in
            
            switch result {
            case .success(let data):
                break
            case .failure(let error):
                print(error)
                break
            }
            
        }
     
    }
    
    
    func connectWithAPI(endpoint: String, completion: @escaping (Result<Data, Error>) -> Void) -> Bool {
        
        guard let url = URL(string: "http://your-ec2-ip-or-domain\(endpoint)") else {
            
            completion(.failure(NSError(domain: "Invalid URL", code: 0, userInfo: nil)))
            
            return false
            
        }
        
        APIClient.connection.dataTask(with: url) { data, response, error in
            
            
            
        }
        
        return true
        
    }

     
     //check if account associated with ID exists
    func assertAccountExistence() -> Bool {
        
        return true
        
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

