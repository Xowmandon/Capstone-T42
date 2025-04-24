//
//  NativeCallProtocol.swift
//  unhinged-app
//
//  Created by Harry Sho on 4/19/25.
//

import Foundation
import UnityFramework

class NativeCallProtocol : NativeCallsProtocol, ObservableObject {
    
    static let shared = NativeCallProtocol()
    
    @Published var receivedMessage : String = ""
    @Published var didFinishGame : Bool = false
    //@Published var didFinishLoading : Bool = false
    
    var startingState : GameMessageData = GameMessageData(gameIdentifier: .none, stateJSON: "")
    
    //Methods called from Unity
    
    func showHostMainWindow(_ color: String!) {
    }
    
    func didFinishLoadingInstance() { //callback runs when unity is ready to receive starting state
        Unity.shared.startMiniGame(launchMessage: startingState)
    }
    
    func sendGameResult(_ result: NSNumber!) {
        let boolResult = result.boolValue
        print ("RECEIVED MESSAGE FROM UNITY: sendGameResult: \(boolResult)")
        receivedMessage = String(boolResult)
    }
    
    func sendGameSaveData(_ json: String!) {
        let jsonString = json as String
        print("RECIEVED UNITY GAME STATE JSON: \(json)")
        receivedMessage = jsonString
        didFinishGame = true
    }
    
}

