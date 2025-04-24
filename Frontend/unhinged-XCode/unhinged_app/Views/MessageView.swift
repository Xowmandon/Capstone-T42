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
    @EnvironmentObject var appModel : AppModel
    @ObservedObject var unityProxy : NativeCallProtocol = NativeCallProtocol.shared
    
    @State private var messages : [Message]
    @State private var messageText : String = ""
    @State private var showOptionsSheet : Bool = false
    @State private var showGameSheet : Bool = false
    @State private var showUnityPlayer : Bool = false
    @State private var shouldUpdateScrollPosition : Bool = false
    @State var loading : Bool = true
    
    @FocusState var focusedOnKeyboard : Bool
    
    init(profile: Profile, matchId: String){
        self.profile = profile
        self.matchId = matchId
        messages = []
    }
    
    @ViewBuilder
    func messageBubble(message : Message, sentFromClient: Bool) -> some View {
        HStack {
            if sentFromClient{
                Spacer()
            }
            if message.kind == .text{
                Text(message.content)
                    .padding()
                    .foregroundStyle(.white)
                    .background{
                        RoundedRectangle(cornerRadius: 10)
                            .foregroundStyle( sentFromClient ? .blue : .gray)
                    }
                
            } else if message.kind == .game{
                VStack{
                    Image(systemName: "gamecontroller.fill")
                    Button{
                        showUnityPlayer = true
                    } label: {
                        Text("Play Game")
                    }
                    .disabled(sentFromClient)
                }
                .background{
                    RoundedRectangle(cornerRadius: 10)
                        .foregroundStyle( message.sentFromClient ? .blue : .gray)
                }
            }
            if !sentFromClient {
                
                Spacer()
                
            }
        }
        .sheet(isPresented: $showUnityPlayer){
            UnityGameView(message: message, gameType: .none, matchedProfile: profile, matchId: matchId)
                .interactiveDismissDisabled(true)
        }
    }
    
    /*
    @ViewBuilder
    func gameBubble(message : Message) -> some View {
        
        let sentFromClient = message.sentFromClient
        
        HStack{
            if sentFromClient{
                Spacer()
            }
            VStack{
                Image(systemName: "gamecontroller.fill")
                Button{
                    showUnityPlayer = true
                } label: {
                    Text("Play Game")
                }
                .disabled(sentFromClient)
            }
            .background{
                RoundedRectangle(cornerRadius: 10)
                    .foregroundStyle( message.sentFromClient ? .blue : .gray)
            }
            if !sentFromClient {
                
                Spacer()
                
            }
        }
        
    }
    */
    @ViewBuilder
    func gameSelect() -> some View {
        NavigationStack {
            VStack{
                HStack {
                    BackButton()
                        .padding()
                    Text("Select a Game!")
                        .font(Theme.titleFont)
                        .padding(.vertical)
                    Spacer()
                }
                List {
                    ForEach(GameType.activeGames, id: \.self){game in
                        NavigationLink(destination: UnityGameView(message: Message(kind:.game, content: "", sentFromClient: true),
                                                                  gameType: game.self,
                                                                  matchedProfile: profile,
                                                                  matchId: matchId).navigationBarBackButtonHidden())
                        {
                            HStack{
                                Text("\(game.displayName)")
                                    .font(Theme.headerFont)
                                Spacer()
                                Image(systemName: "\(game.imageName)")
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
    }
    var body: some View {
        ZStack {
            VStack {
                // MARK: Top Bar
                HStack{
                    BackButton()
                    Spacer()
                    //NavigationLink(destination: ProfileView()){ }
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
                .frame(maxHeight: 50)
                .padding()
                .background{
                    CardBackground()
                }
                // MARK: Message Bubbles
                if !loading {
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
                        .padding(.horizontal)
                        .onChange(of: focusedOnKeyboard) {
                            if focusedOnKeyboard {
                                DispatchQueue.main.asyncAfter(deadline: .now() + 0.05){
                                    shouldUpdateScrollPosition = true
                                }
                            }
                        }
                        .onChange(of: shouldUpdateScrollPosition) {
                             // Auto-scroll when new messages appear
                             DispatchQueue.main.asyncAfter(deadline: .now() + 0.05){
                                 if shouldUpdateScrollPosition {
                                     withAnimation {
                                         proxy.scrollTo("bottom", anchor: .bottom)
                                     }
                                     shouldUpdateScrollPosition = false
                                 }
                             }
                        }
                    }
                } else {
                    VStack {
                        Spacer()
                        ProgressView("Getting your messages...")
                        Spacer()
                    }
                }
                // MARK: Message Field
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
                DispatchQueue.main.async{
                    focusedOnKeyboard = false
                    shouldUpdateScrollPosition = true
                }
            }
        }
        .toolbar{
            ToolbarItemGroup (placement: .keyboard) {
                HStack {
                    Button{
                        showGameSheet.toggle()
                        focusedOnKeyboard = false
                    } label: {
                        Image(systemName: "gamecontroller.fill")
                        Text("Press Start!")
                            .font(Theme.bodyFont)
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
                        Text("You matched on <DATE>")
                        Text("X Messages")
                        Text("X Games Played")
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
        .onAppear{
            fetchMessages()
        }
        // MARK: Game Entry Point
        .fullScreenCover(isPresented: $showGameSheet){
            gameSelect()
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
            loading = true
            messages = await APIClient.shared.getConversationMessages(match_id: self.matchId, limit: nil, page: nil, all_messages: true)
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.05){
                shouldUpdateScrollPosition = true
            }
            loading = false
        }
    }
}

#Preview {
    //MessageView(profile: Profile(), matchId: "")
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
    //MessageView(profile: Profile(), matchId: "1")
}
