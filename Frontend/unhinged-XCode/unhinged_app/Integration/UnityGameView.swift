//
//  UnityGameView.swift
//  unhinged-app
//
//  Created by Harry Sho on 4/20/25.
//


import Foundation
import SwiftUI



struct UnityGameView: View {
    
    private var unity = Unity.shared
    
    @Binding var showGameSheet : Bool
    @ObservedObject var proxy : NativeCallProtocol = NativeCallProtocol.shared
    @EnvironmentObject var appModel : AppModel
    
    let message : Message
    let gameType : GameType //Used only from game start sheet
    let matchedProfile : Profile
    let matchId : String
    
    @State var loading : Bool = false
    
    init(message: Message, gameType: GameType, matchedProfile: Profile, matchId : String, showGameSheet: Binding<Bool>) {
        self.message = message
        self.gameType = gameType
        self.matchedProfile = matchedProfile
        self.matchId = matchId
        self._showGameSheet = showGameSheet
    }
    
    var body: some View {
        ZStack {
            if loading {
                // Unity is starting up or shutting down
                ProgressView("Loading...").foregroundStyle(.primary)
            } else if let UnityContainer = unity.view.flatMap({ UIViewContainer(view: $0) }) {
                UnityContainer
                    .ignoresSafeArea()
                VStack{
                    Spacer()
                    Button("Stop Game", systemImage: "stop", action: {
                        loading = true
                        DispatchQueue.main.async(execute: {
                            unity.stop()
                            loading = false
                        })
                    })
                    
                }
            } else {
                Button("Start Game", systemImage: "play", action: {
                    launchGame()
                })
            }
            VStack{
                HStack{
                    BackButton()
                        .padding()
                        .frame(maxWidth: 30)
                    Spacer()
                }
                Spacer()
            }
        }
        .onDisappear{
            print("send message if finished game")
            finishGame()
        }
    }
    
    func launchGame() {
        
        var gameData : GameMessageData = GameMessageData(gameIdentifier: gameType, stateJSON: "")
        do {
            if !message.sentFromClient{ // Get game state from message data
                gameData = try JSONDecoder().decode(GameMessageData.self, from: Data(message.content.utf8))
            } else { // Create game state structure and encode
                let stateStruct = GameType.createGameStateStructure(gameType: gameType,
                                                                    clientPlayerProfile: appModel.profile,
                                                                    matchedPlayerProfile: matchedProfile)
                let stateJSON = try JSONEncoder().encode(stateStruct)
                gameData.game_state = String(data: stateJSON, encoding: .utf8)!
            }
            DispatchQueue.main.async(execute: {
                loading = true
                proxy.gameType = gameData.game_name
                proxy.startingState = gameData
                unity.start() //Start Client
                loading = false
            })
            
        } catch {
            print("Launch game failed: \(error)")
        }
    }
    
    func finishGame() {
        
        if proxy.didFinishGame {
            
            print("Game finished")
            Task{
                var gameData : GameMessageData = GameMessageData(gameIdentifier: gameType, stateJSON: "")
                gameData.game_state = proxy.receivedMessage
                let gameMessageData = try! JSONEncoder().encode(gameData)
                let gameMessageString = String(data: gameMessageData, encoding: .utf8)!
                print("SENT GAME STATE MESSAGE: \(gameMessageString)")
                await APIClient.shared.pushConversationMessage(match_id: matchId, msgType: Message.Kind.game, content: gameMessageString)
            }
            showGameSheet = false
            proxy.didFinishGame = false
        }
    }
    
}
