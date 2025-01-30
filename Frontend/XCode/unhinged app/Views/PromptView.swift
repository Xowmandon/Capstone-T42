//
//  PromptView.swift
//  unhinged app
//
//  Created by Harry Sho on 1/23/25.
//

import Foundation
import SwiftUI

struct PromptView : View {
    
    let prompt : PromptItem
    let Icons : [String] = ["checkmark", "xmark"]
    
    @State var selectedChoice : PromptChoice.ID?
    @State var didConfirmChoice : Bool = false
    
    @ViewBuilder func confirmButton() -> some View {
        Button(action: {
            didConfirmChoice.toggle()
        }) {
            
            HStack {
                Spacer()
                Text(didConfirmChoice ? "Try Again" : "Confirm")
                    .padding()
                Spacer()
            }
            .background {
                RoundedRectangle(cornerRadius: 4, style: .continuous)
                    .fill(.placeholder.opacity(0.5))
            }
            .padding()
        }
    }
    
    @ViewBuilder func choiceButton(option: PromptChoice, isSelected: Bool, isCorrect: Bool, showAnswer: Binding<Bool>) -> some View {
        
        Button(action: {
            
            selectedChoice = option.id
            
        }){
           
            // choice row
            HStack {
                if(showAnswer.wrappedValue == true) {
                    Image(systemName: isSelected && isCorrect ? "checkmark.square.fill" : "xmark").font(.title)
                        .padding(.horizontal)
                } else {
                    
                    Image(systemName: isSelected ? "circle.fill" : "circle")
                        .padding(.horizontal)
                    
                }
                Text(option.choice)
                    .padding()
                    .foregroundStyle(.primary)
                    .clipped()
                Spacer()
            }
            .background {
                RoundedRectangle(cornerRadius: 4, style: .continuous)
                    .foregroundStyle(.regularMaterial)
            }
            .padding(.horizontal)
            
        }
        
    }
    
    var body: some View {
        VStack {
            // Prompt
            HStack {
                Text(prompt.question)
                    .font(.headline)
                Spacer()
            }
            .padding()
            VStack(spacing: 10) {
                ForEach(prompt.choices){option in
                    
                    choiceButton(
                        option: option,
                        isSelected: selectedChoice == option.id ? true : false,
                        isCorrect: option.id == prompt.correctChoice ? true : false,
                        showAnswer: $didConfirmChoice
                    )
                    
                }
                
                confirmButton()
                
                
            }
            .padding(.bottom)
            
        }
        .background {
            RoundedRectangle(cornerRadius: 20, style: .continuous)
                .foregroundStyle(.regularMaterial)
        }
    }
    
}


#Preview {
    
    let prompt_choices : [PromptChoice] = [
        PromptChoice(id: UUID(), isSelected: false, choice: "Choice 1"),
        PromptChoice(id: UUID(), isSelected: false, choice: "Choice 1"),
        PromptChoice(id: UUID(), isSelected: false, choice: "Choice 1")
    ]
    
    PromptView(prompt: PromptItem(question: "Choose", choices: prompt_choices, correctChoice: prompt_choices[0].id), selectedChoice: prompt_choices[0].id)
               
}
