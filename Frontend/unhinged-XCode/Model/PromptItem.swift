//
//  ProfileItem.swift
//  unhinged app
//
//  Created by Harry Sho on 1/23/25.
//

import Foundation

class PromptItem : Identifiable {
    
    let id: UUID
    let question: String
    let choices: [PromptChoice]
    let correctChoice: PromptChoice.ID
    
    init(question: String, choices: [PromptChoice], correctChoice: UUID){
        self.id = UUID()
        self.question = question
        self.choices = choices
        self.correctChoice = correctChoice
        
    }
}

struct PromptChoice : Identifiable {
    
    var id: UUID
    var isSelected: Bool
    let choice: String
    
}

