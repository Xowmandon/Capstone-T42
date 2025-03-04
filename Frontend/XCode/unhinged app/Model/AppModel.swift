//
//  AppModel.swift
//  unhinged app
//
//  Created by Harry Sho on 12/8/24.
//

import Foundation
import SwiftUI

final class AppModel : ObservableObject {
    
    @Published var prospectiveMatches : [Profile]
    
    @Published var conversations : [Conversation]
    
    init() {
        
        self.prospectiveMatches = AppModel.getMatches()
        self.conversations = []
        
    }
    
    static func getMatches() -> [Profile] {
        
        //Fetch
        let test_prompt_choices : [PromptChoice] = [
            PromptChoice(id: UUID(), isSelected: false, choice: "Choice 1"),
            PromptChoice(id: UUID(), isSelected: false, choice: "Choice 1"),
            PromptChoice(id: UUID(), isSelected: false, choice: "Choice 1")
        ]
        
        let test_prompt = PromptItem(question: "Test Prompt", choices: test_prompt_choices, correctChoice: test_prompt_choices[0].id)
        let test_prompt2 = PromptItem(question: "Test Prompt", choices: test_prompt_choices, correctChoice: test_prompt_choices[2].id)
        
        let prompt_profile = Profile(name: "John Doesington", imageName: "stockPhoto")
        
        prompt_profile.addPrompts(promptList: [test_prompt, test_prompt2])
        
        let matches = [prompt_profile, Profile(), Profile(name: "john doe1", imageName: "stockPhoto"), Profile(name: "john doe2", imageName: "stockPhoto")]
        
        return matches
    }
    
}
