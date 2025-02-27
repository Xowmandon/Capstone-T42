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
    @State private var messages : [Message]
    @State private var messageText : String = ""
    @State private var showOptionsSheet : Bool = false
    @State private var showGameSheet : Bool = false
    
    let games : [GameObject] = GameObject.gameList
    
    init(profile: Profile){
        self.profile = profile
        _messages = State(initialValue: MessageView.fetchMessages())
    }
    
    @ViewBuilder
    func messageBubble(message : Message, sentFromClient: Bool) -> some View{
        HStack {
            if sentFromClient{
                Spacer()
            }
            Text(message.content)
                .padding()
                .foregroundStyle(.white)
                .background{
                    RoundedRectangle(cornerRadius: 10)
                        .foregroundStyle( sentFromClient ? .blue : .gray)
                }
                .padding()
            if !sentFromClient {
                
                Spacer()
                
            }
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
                    VStack{
                        ForEach(messages) {message in
                            messageBubble(message: message, sentFromClient: message.sentFromClient)
                                .border(.black, width: 1)
                            
                        }
                    }
                    
                }
                HStack{
                    Button(action: {
                        
                        showGameSheet.toggle()
                        // assert unity instance
                        // prepare game state message
                        // Present unity window to windowgroup using Unity framework
                        // pass game state to Unity instance
                    }, label: {
                        Text("Press Start!")
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
                //present options sheet
                Button(action: {showOptionsSheet.toggle()} ){
                    Image(systemName: "ellipsis")
                        .foregroundStyle(.primary)
                }
            }
        }
        .sheet(isPresented: $showOptionsSheet) {
            
            VStack{
                VStack {
                    VStack(spacing: 10) {
                        Spacer()
                        Spacer()
                            .foregroundStyle(.primary)
                            .font(.headline)
                        Text("Conversation with \(profile.name)")
                        Text("You matched on November 17, 2024")
                        Text("27 Messages")
                        Text("5 Games Played")
                        Spacer()
                        // Email
                        HStack(alignment: .firstTextBaseline) {
                            Image(systemName: "flag.fill")
                                .imageScale(.medium)
                                .symbolRenderingMode(.monochrome)
                            Text("Report Account")
                        }
                        .font(.system(.body, weight: .medium))
                        .padding(.vertical, 16)
                        .frame(maxWidth: .infinity)
                        .clipped()
                        .foregroundStyle(.orange)
                        .background {
                            RoundedRectangle(cornerRadius: 10, style: .continuous)
                                .stroke(.clear.opacity(0.25), lineWidth: 0)
                                .background(RoundedRectangle(cornerRadius: 10, style: .continuous).fill(.yellow.opacity(0.15)))
                        }
                    }
                    .padding(20)
                    Spacer()
                }
                .padding(.vertical, 70)
                
            }
            
        }
        .sheet(isPresented: $showGameSheet){
            VStack{
                Text("Select a Game!")
                    .font(Theme.titleFont)
                
                ForEach(games){gameObject in
                    HStack{
                        Text("\(gameObject.name)")
                            .font(Theme.headerFont)
                        Spacer()
                        Image(systemName: "\(gameObject.imageName)")
                            .resizable()
                            .scaledToFit()
                            .frame(maxWidth: 50)
                            .foregroundStyle(.blue)
                    }
                    .padding()
                    .background{
                        CardBackground()
                    }
                }
            }
        }
    }
    private func sendMesage() {
        // push message
        messageText = ""
        //APIClient.shared.sendMesage(text: messageText)
    }
    private static func fetchMessages() -> [Message]{
        //
        APIClient.shared
        return [Message(), Message(), Message(sentFromClient: true)]
    }
}

#Preview {
    MessageView(profile: Profile())
}


/*
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

*/
