//
//  Conversation.swift
//  unhinged app
//
//  Created by Harry Sho on 11/7/24.
//

import Foundation

struct Conversation : Identifiable {
    
    //TODO: Make codable
    
    //Backend Fields
    var matchId : String? //For the client/recipient pair of users
    var matchedUserId : String? // Matched user
    
    var matchedName : String? //Matched user's name
    var matchDate : String?
    var lastMessage : String?
    
    //Local Fields
    var id : UUID = UUID()
    var matchedProfile: Profile
    var messages : [Message] = []
    
    var hasUnreadMessages : Bool = false
}
