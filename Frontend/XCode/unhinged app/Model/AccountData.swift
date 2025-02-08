//
//  AccountData.swift
//  unhinged app
//
//  Created by Harry Sho on 12/9/24.
//

import Foundation

final class AccountData {
    
    static let shared = AccountData(hasBeenAuthenticated: false, email: "") // Singleton for client's account
    
    private var hasBeenAuthenticated : Bool = false
    
    private var userID : String?
    
    private var email : String
    
    private var profile : Profile? 
    
    init(hasBeenAuthenticated: Bool, userID: String? = nil, email: String, profile: Profile? = nil) {
        self.hasBeenAuthenticated = hasBeenAuthenticated
        self.userID = userID
        self.email = email
        self.profile = profile
    }
    
    func getUserID() -> String? {
        return self.userID
    }
    
    func authenticate() -> Void {
        AccountData.shared.hasBeenAuthenticated = true
    }
    
    func setUserID(_ newUserID: String?) {
        self.userID = newUserID
    }

    func getEmail() -> String? {
        return self.email
    }
    
    func setEmail(_ newEmail: String) {
        self.email = newEmail
    }

    func setProfile(_ newProfile: Profile?) {
        self.profile = newProfile
    }
    
    func getProfile() -> Profile? {
        return self.profile
    }
    
    
}
