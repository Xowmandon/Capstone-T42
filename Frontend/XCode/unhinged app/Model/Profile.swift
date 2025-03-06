//
//  Profile.swift
//  unhinged app
//
//  Created by Harry Sho on 11/7/24.
//

import Foundation
import SwiftUI

class Profile : Identifiable {
    
    static let clientProfile : Profile = Profile()
    
    var ID : UUID = UUID()
    
    var name : String = "John Doe"
    
    var age : Int = 18
    
    var image : Image = Image("stockPhoto")
    
    var attributes : [Attribute] = [Attribute(customName: "He/Him", symbolName: "person")]
    
    var biography : String? = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia"
    
    var gender : String? = "male"
    
    var prompts : [PromptItem]?
    
    private var userIdentifyingEmail : String?
    
    init(){}
    
    init(name: String, image: Image = Image(systemName: "person.fill")) {
        self.name = name
        self.image = image
    }
    
    func addPrompts(promptList : [PromptItem]){
        self.prompts = promptList
    }
    
}
