//
//  GameObject.swift
//  unhinged app
//
//  Created by Harry Sho on 2/20/25.
//

import Foundation

enum GameType : String, Codable, CaseIterable {
    // rawvalue is Scene name
    case none = "None"
    case ghosted = "Ghosted"
    case ghostHunter = "GhostHunter"
    case heartfall = "Heartfall"
    case memoryMatch = "MemoryMatch"
    case redFlagRacing = "RedFlagRacing"
    case rpgBattle = "RPGBattle"
    case ticTacToe = "TicTacToe"
    case wipeTheIck = "WipeTheIck"
    
    static var activeGames : [GameType] {
        
        return [.ticTacToe]
        
    }
    
    var displayName : String {
        switch self {
            case .none:         return "None"
            case .ghosted:      return "Ghosted"
            case .ghostHunter:  return "Ghost Hunter"
            case .heartfall:    return "Heartfall"
            case .memoryMatch:  return "Memory Match"
            case .redFlagRacing: return "Red Flag Racing"
            case .rpgBattle:    return "RPG Battle"
            case .ticTacToe:    return "Tic-Tac-Toe"
            case .wipeTheIck:   return "Wipe the Ick"
        }
    }
    
    var imageName : String {
        return "gamecontroller.circle.fill"
    }
    
    struct ticTacToeData : Codable {
        var winner      : String?   = nil
        var boardState  : [String]  = ["", "", "",
                                       "", "", "",
                                       "", "", ""]
        var nameP1      : String    = ""
        var nameP2      : String    = ""
        var playerNum   : Int       = 1
    }
    
    static func createGameStateStructure (gameType : GameType, clientPlayerProfile : Profile, matchedPlayerProfile : Profile) -> Codable {
        switch gameType {
        case .none:
            return 0
        case .ghosted:
            return 0
        case .ghostHunter:
            return 0
        case .heartfall:
            return 0
        case .memoryMatch:
            return 0
        case .redFlagRacing:
            return 0
        case .rpgBattle:
            return 0
        case .ticTacToe:
            return ticTacToeData()
        case .wipeTheIck:
            return 0
        }
     
    }
    
    
    /*static func decodeStateJSON(gameType: GameType, dataJSON: String) throws {
        
        switch gameType {
        case .none:
            break
        case .ticTacToe:
            break
        case .ghosted:
            break
        case .ghostHunter:
            break
        case .heartfall:
            break
        case .memoryMatch:
            break
        case .redFlagRacing:
            break
        case .rpgBattle:
            break
        case .wipeTheIck:
            break
        }
        
    }
     */
    
}

struct GameMessageData: Codable {
    var gameIdentifier: GameType
    var stateJSON: String
    
    init(gameIdentifier: GameType, stateJSON: String) {
        self.gameIdentifier = gameIdentifier
        self.stateJSON = stateJSON
    }
}

/*
struct GameObject : Identifiable {
    
    let id : UUID = UUID()
    let type : GameType
    
}
*/
