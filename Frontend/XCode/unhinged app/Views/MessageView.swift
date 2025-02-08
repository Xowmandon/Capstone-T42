//
//  MessageView.swift
//  unhinged app
//
//  Created by Harry Sho on 11/25/24.
//
//
//

import Foundation
import SwiftUI

struct MessageView : View {
    
    let profile : Profile
    
    //@EnvironmentObject var appModel : AppModel
    
    @State private var messages : [Message] = [Message(), Message(), Message()]
    @State private var messageText : String = ""
    
    init(profile: Profile){
        
        self.profile = profile
        self.messages = []
        self.messages = fetchMessages()
    }
    
    @ViewBuilder
    func messageBubble(message : Message) -> some View{
        
        HStack {
            
            Text(message.content)
                .padding()
                .foregroundStyle(.white)
                .background{
                    
                    RoundedRectangle(cornerRadius: 10)
                        .foregroundStyle(.blue)
                }
                .padding()
            
            Spacer()
        }
        
    }
    
    var body: some View {
        
        ZStack {
            
            VStack {
                
                HStack{
                    
                    Image(profile.imageName)
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .frame(width: 40, height: 40)
                        .clipShape(Circle())
                    
                    Text(profile.name)
                    
                }
                
                ScrollView{
                    
                    List(messages){message in
                        
                        Text("a")
                        
                    }
                        
                    messageBubble(message: messages[0])
                        .border(.black, width: 1)
                    
                    
                }
                HStack{
                    
                    Button(action: {
                        
                        // assert unity instance
                        
                        // prepare game state message
                        
                        // Present unity window to windowgroup using Unity framework
                        
                        // pass game state to Unity instance
                        
                    }, label: {
                        
                        Text("Start Game!")
                        
                    })
                    
                }
                HStack{
                    
                    TextField("Send a message", text: $messageText)
                        .textFieldStyle(.roundedBorder)
                        .padding()
                    Button(action: {
                        sendMesage()
                    }, label:{
                        
                        Image(systemName: "paperplane.fill")
                            .foregroundStyle(.primary)
                            .font(.title2)
                    })
                    .padding(.trailing)
                    
                }
                .background{
                    
                    Rectangle()
                        .foregroundStyle(.regularMaterial)
                }
                .frame(maxHeight: 100)
            }
        }
        .toolbar{
            
            ToolbarItem(placement: .topBarTrailing){
                
                Image(systemName: "ellipsis")
                    .foregroundStyle(.primary)
                
            }
            
            
        }
    }
    
    private func sendMesage() {
        
        // push message
        
        messageText = ""
        
        //APIClient.shared.sendMesage(text: messageText)
        
    }
    
    private func fetchMessages() -> [Message]{
        
        //
        
        APIClient.shared
        
        
        return [Message(), Message(), Message()]
        
    }
    
}


#Preview {
    MessageView(profile: Profile())
}

