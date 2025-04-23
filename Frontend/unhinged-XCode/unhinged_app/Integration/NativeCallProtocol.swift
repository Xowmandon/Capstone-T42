//
//  NativeCallProtocol.swift
//  unhinged-app
//
//  Created by Harry Sho on 4/19/25.
//

import Foundation
import UnityFramework

class NativeCallProtocol : NativeCallsProtocol {
    
    static let shared = NativeCallProtocol()
    
    func showHostMainWindow(_ color: String!) {
    }
    
    func sendGameResult(_ result: Bool!) {
        print ("RECEIVED MESSAGE FROM UNITY: sendGameResult: \(result!)")
    }
    
}

