//
//  ProfileItem.swift
//  unhinged app
//
//  Created by Harry Sho on 1/23/25.
//

import Foundation

struct PromptItem : Identifiable, Codable {
    static let examplePromptChoices : [PromptChoice] = [PromptChoice(choice: "Duck"),
                                                        PromptChoice(choice: "Duck"),
                                                        PromptChoice(choice: "Goose")]
        
    static let examplePrompt : PromptItem = PromptItem(
        
        question: "Two Truths and a Lie",
        choices: examplePromptChoices,
        correctChoiceUUID: examplePromptChoices.last!.id
    
    )
    
    var id: UUID = UUID()
    let question: String
    let choices: [PromptChoice]
    let correctChoice: PromptChoice.ID
    
    init(question: String, choices: [PromptChoice], correctChoiceUUID: UUID){
        self.id = UUID()
        self.question = question
        self.choices = choices
        self.correctChoice = correctChoiceUUID
        
    }
    
}

struct PromptChoice : Identifiable, Codable {
    
    var id: UUID = UUID()
    let choice: String
    var isSelected: Bool = false
    
    enum CodingKeys: CodingKey {
        case id
        case choice
    }
    
}

