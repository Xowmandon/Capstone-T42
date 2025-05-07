//
//  PromptFormView.swift
//  unhinged app
//
//  Created by Harry Sho on 4/13/25.
//

import SwiftUI

struct PromptFormView: View {
    
    
    @Binding var presentationMode : PresentationMode
    @Binding var promptList : [PromptItem]
    @State private var question: String = ""
    @State private var correctAnswer: String = ""
    @State private var incorrectAnswers: [String] = [""]
    
    var body: some View {
        HStack{
            BackButton()
            Spacer()
            Text("Create a Prompt")
                .font(Theme.titleFont)
            Spacer()
        }
        .padding()
        Form {
            Section(header: Text("Question")){
                TextField("Ask possible matches anything", text: $question)
            }
            Section(header: Text("Correct Answer")) {
                TextField("Enter the correct answer to your prompt", text: $correctAnswer)
            }
            
            Section(header: Text("Incorrect Answers")) {
                ForEach(incorrectAnswers.indices, id: \.self) { index in
                    HStack {
                        TextField("Throw off your matches with incorrect options", text: $incorrectAnswers[index])
                        Button(action: {
                            incorrectAnswers.remove(at: index)
                        }) {
                            Image(systemName: "minus.circle")
                                .foregroundColor(.red)
                        }
                        .disabled(incorrectAnswers.count <= 1)
                    }
                }
                
                if incorrectAnswers.count < 10 {
                    Button(action: {
                        incorrectAnswers.append("")
                    }) {
                        Label("Add Incorrect Answer", systemImage: "plus.circle")
                    }
                }
            }
            
            Button{
                finishCreatingPrompt()
            } label: {
                Text("Confirm")
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background{
                        CardBackground()
                    }
            }
            
        }
        
    }
    
    // Computed properties for final output
    var correct: [String] {
        correctAnswer.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty ? [] : [correctAnswer]
    }
    
    var incorrect: [String] {
        incorrectAnswers.map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }.filter { !$0.isEmpty }
    }
    
    func finishCreatingPrompt(){
        
        var choices : [PromptChoice] = []
        for incorrectAnswer in incorrectAnswers {
            choices.append(PromptChoice(choice: incorrectAnswer))
        }
        
        let correctChoice = PromptChoice(choice: correctAnswer)
        let correctID = correctChoice.id
        choices.append(correctChoice)
        
        let newPrompt = PromptItem(question: question, choices: choices, correctChoiceUUID: correctID)
        
        promptList.append(newPrompt)
        presentationMode.dismiss()
        
    }
}

#Preview {
    
    //PromptFormView(promptList: State(initialValue: [PromptItem.examplePrompt]))
}
