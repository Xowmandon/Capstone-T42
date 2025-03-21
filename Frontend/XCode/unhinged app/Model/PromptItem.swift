//
//  ProfileItem.swift
//  unhinged app
//
//  Created by Harry Sho on 1/23/25.
//

import Foundation

class PromptItem : Identifiable {
    
    static let examplePromptChoices : [PromptChoice] = [PromptChoice(choice: "Duck"),
                                                        PromptChoice(choice: "Duck"),
                                                        PromptChoice(choice: "Goose")]
        
    static let examplePrompt : PromptItem = PromptItem(
        
        question: "Two Truths and a Lie",
        choices: examplePromptChoices,
        correctChoice: examplePromptChoices.last!.id
    
    )
    
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
    
    var id: UUID = UUID()
    var isSelected: Bool = false
    let choice: String
    
}

