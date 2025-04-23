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
    let matchId : String
    //@EnvironmentObject var appModel : AppModel
    @State private var messages : [Message]
    @State private var messageText : String = ""
    @State private var showOptionsSheet : Bool = false
    @State private var showGameSheet : Bool = false
    @State private var shouldUpdateScrollPosition : Bool = false
    
    @FocusState var focusedOnKeyboard : Bool
    
    let games : [GameObject] = GameObject.gameList
    
    init(profile: Profile, matchId: String){
        self.profile = profile
        self.matchId = matchId
        messages = []
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
    
    @ViewBuilder
    func gameSelect(games: [GameObject]) -> some View {
        NavigationStack {
            VStack{
                Text("Select a Game!")
                    .font(Theme.titleFont)
                
                List(games){gameObject in
                    NavigationLink(destination: UnityGameView()){
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
    }
    var body: some View {
        ZStack {
            VStack {
                // MARK: Message Bubbles
                ScrollViewReader { proxy in
                    ScrollView{
                        
                        if !messages.isEmpty {
                            VStack{
                                ForEach(messages.reversed()) {message in
                                    messageBubble(message: message, sentFromClient: message.sentFromClient)
                                }
                                Color.clear.id("bottom")
                                    .frame(maxHeight: 1)
                            }
                        } else {
                            Image(uiImage: UIImage(named: "Speech_bubble")!.withRenderingMode(.alwaysTemplate))
                                .foregroundColor(.gray)
                                .foregroundStyle(.tertiary)
                            Text("No messages yet!")
                                .foregroundStyle(.secondary)
                            
                        }
                        
                    }
                     .onAppear {
                        fetchMessages()
                        proxy.scrollTo("bottom", anchor: .bottom)
                    }
                     .onChange(of: shouldUpdateScrollPosition) {
                         // Auto-scroll when new messages appear
                         DispatchQueue.main.async {
                             if shouldUpdateScrollPosition {
                                 withAnimation {
                                     proxy.scrollTo("bottom", anchor: .bottom)
                                 }
                             }
                         }
                         shouldUpdateScrollPosition.toggle()
                    }
                }
                HStack{
                    TextField("Send a message", text: $messageText)
                        .focused($focusedOnKeyboard, equals: true)
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
            .onTapGesture {
                focusedOnKeyboard = false
            }
        }
        .toolbar{
            ToolbarItem(placement: .principal){
                HStack{
                    BackButton()
                    Spacer()
                    profile.image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .frame(width: 40, height: 40)
                        .clipShape(Circle())
                    Text(profile.name)
                        .font(Theme.headerFont)
                    Spacer()
                    //present options sheet
                    Button(action: {showOptionsSheet.toggle()} ){
                        Image(systemName: "ellipsis")
                            .foregroundStyle(.primary)
                    }
                }
                .padding()
                .background{
                    CardBackground()
                }
                .offset(y: 20)
            }
            ToolbarItemGroup (placement: .keyboard) {
                HStack {
                    Button{
                        showGameSheet.toggle()
                    } label: {
                        Text("Press Start!")
                            .font(Theme.bodyFont)
                        Image(systemName: "gamecontroller.fill")
                        Spacer()
                    }
                    Spacer()
                    Button() {
                        focusedOnKeyboard = false // Dismiss keyboard
                    } label: {
                        Spacer()
                        Image(systemName: "checkmark.circle.fill")
                    }
                }
            }
        }
        // MARK: Options
        .sheet(isPresented: $showOptionsSheet) {
            
            VStack{
                VStack {
                    VStack(spacing: 10) {
                        Spacer()
                        Spacer()
                            .foregroundStyle(.primary)
                            .font(.headline)
                        Text("Conversation with \(profile.name)")
                        //Metrics
                        Text("You matched on November 17, 2024")
                        Text("27 Messages")
                        Text("5 Games Played")
                        Spacer()
                        // Report Button
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
        // MARK: Game Entry Point
        .sheet(isPresented: $showGameSheet){
            gameSelect(games: games)
        }
        .navigationBarBackButtonHidden()
    }
    private func sendMesage() {
        // push message
        if !messageText.isEmpty {
            Task {
                await APIClient.shared.pushConversationMessage(match_id: matchId , type: Message.Kind.text, content: messageText)
                messageText = ""
                fetchMessages();
            }
        }
        
    }
    private func fetchMessages() {
        Task{
            messages = await APIClient.shared.getConversationMessages(match_id: self.matchId, limit: nil, page: nil, all_messages: true)
            shouldUpdateScrollPosition.toggle()
        }
    }
}

#Preview {
    MessageView(profile: Profile(), matchId: "")
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


*/

#Preview {
    MessageView(profile: Profile(), matchId: "1")
}
