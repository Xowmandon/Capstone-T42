//
//  Profile.swift
//  unhinged app
//
//  Created by Harry Sho on 11/7/24.
//

import Foundation

class Profile : Identifiable {
    
    var ID : UUID = UUID()
    
    var name : String = "John Doe"
    
    var imageName : String = "stockPhoto"
    
    var attributes : [Attribute] = [Attribute(customName: "He/Him", symbolName: "person")]
    
    var biography : String? = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia"
    
    var gender : String? = "male"
    
    var prompts : [PromptItem]?
    
    
    private var userIdentifyingEmail : String?
    
    init(){}
    
    init(name: String, imageName: String) {
        self.name = name
        self.imageName = imageName
    }
    
    func addPrompts(promptList : [PromptItem]){
        self.prompts = promptList
    }
    
}
