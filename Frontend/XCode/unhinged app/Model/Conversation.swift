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
    var match_id : String? //For the client/recipient pair of users
    var matched_user_id : String? // Matched user
    
    var matched_user_name : String? //Matched user's name
    var match_date : String?
    var last_message : String?
    
    //Local Fields
    var id : UUID = UUID()
    var recipient: Profile = Profile()
    var messages : [Message] = []
    
    var hasUnreadMessages : Bool = false
}
