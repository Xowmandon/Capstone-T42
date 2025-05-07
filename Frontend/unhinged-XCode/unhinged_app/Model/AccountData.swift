//
//  AccountData.swift
//  unhinged app
//
//  Created by Harry Sho on 12/9/24.
//

import Foundation

final class AccountData {
    
    static let shared = AccountData()
    
    init(){}
    
    var fullName: String {
        let defaults = UserDefaults.standard
        
        if  let first = defaults.string(forKey: "UserFirstName"),
            let last = defaults.string(forKey: "UserLastName") {
         
            return String("\(first) \(last)")
            
        }
        
        return "No Name"
        
    }
    
    var isFirstLogin: Bool {
        let defaults = UserDefaults.standard
        let hasLoggedInBefore = defaults.bool(forKey: "UserHasLoggedInBefore")
        return !hasLoggedInBefore
    }
    
    func finishedFirstTimeSetup () {
        let defaults = UserDefaults.standard
        let hasLoggedInBefore = defaults.bool(forKey: "UserHasLoggedInBefore")
        if !hasLoggedInBefore {
            defaults.set(true, forKey: "UserHasLoggedInBefore")
        }
    }
    
}
