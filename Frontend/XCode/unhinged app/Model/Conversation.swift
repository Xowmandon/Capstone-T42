//
//  Conversation.swift
//  unhinged app
//
//  Created by Harry Sho on 11/7/24.
//

import Foundation

struct Conversation : Identifiable {
    
    var id : String = UUID().uuidString
    var recipient: Profile = Profile()
    var messages : [Message] = []
    
    var hasUnreadMessages : Bool = false
    
    
}
