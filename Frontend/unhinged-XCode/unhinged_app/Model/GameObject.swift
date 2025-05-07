//
//  GameObject.swift
//  unhinged app
//
//  Created by Harry Sho on 2/20/25.
//

import Foundation

enum GameType: String, Codable, CaseIterable {
    // rawValue is Scene name
    case none          = "None"
    case ghosted       = "Ghosted"
    case ghostHunter   = "GhostHunter"
    case heartfall     = "Heartfall"
    case memoryMatch   = "MemoryMatch"
    case redFlagRacing = "RedFlagRacing"
    case rpgBattle     = "RPGBattle"
    case ticTacToe     = "TicTacToe"
    case wipeTheIck    = "WipeTheIck"

    static var activeGames: [GameType] {
        return GameType.allCases.filter {
            ![.none, .memoryMatch, .wipeTheIck].contains($0)
        }
        //[.ticTacToe, .rpgBattle, .redFlagRacing]
    }

    var displayName: String {
        switch self {
        case .none:         return "None"
        case .ghosted:      return "Ghosted"
        case .ghostHunter:  return "Ghost Hunter"
        case .heartfall:    return "Heartfall"
        case .memoryMatch:  return "Memory Match"
        case .redFlagRacing:return "Red Flag Racing"
        case .rpgBattle:    return "RPG Battle"
        case .ticTacToe:    return "Tic-Tac-Toe"
        case .wipeTheIck:   return "Wipe the Ick"
        }
    }

    var imageName: String { "gamecontroller.circle.fill" }
    
    var emoji: String {
        switch self {
        case .none:          return "❓"
        case .ghosted:       return "👻"
        case .ghostHunter:   return "🔦"
        case .heartfall:     return "💔"
        case .memoryMatch:   return "🧠"
        case .redFlagRacing: return "🏁"
        case .rpgBattle:     return "⚔️"
        case .ticTacToe:     return "🔲"
        case .wipeTheIck:    return "🧼"
        }
    }

    // MARK: RFR State
    struct RFRGameState: Codable {
        var answers: [Bool]      // 5 rounds
        var prompt: [String]
        var masterSeed: Int
    }
    
    // MARK: – RPG battle state
    struct RPGState: Codable {
        var playerNames: [String]
        var bossId: String
        var playerTurn: Int
        var playerNum: Int
        var lastPlayerMove: moveType
        var playerHPs: [Float]
        var playerStatuses: [StatusType]
        var playerStatusDurations: [Int]
        var bossHP: Float
        var bossStatus: StatusType
        var bossStatusDuration: Int
        var randomSeed: Int
        var playersWon: Bool
        var myPlayerIndex: Int  // 0 for player 1, 1 for player 2
    }
    enum moveType : Codable {
        case None
        case Melee
        case Magic
        case Heal
        case Ultimate
    }
    enum StatusType : Codable {
        case none
        case HeartBroken
        case Ghosted
        case Lovebombed
    }
    enum BossType : String, Codable, CaseIterable {
        case Ricardio       = "Ricardio"
        case TheAlgorithm   = "TheAlgorithm"
        case LovebombTed    = "LovebombTed"
    }

    // MARK: – Tic-Tac-Toe state
    struct TicTacToeData: Codable {
        var winner: String?    = ""
        var boardState: [String] = Array(repeating: "", count: 9)
        var nameP1: String     = ""
        var nameP2: String     = ""
        var lastMoveBy: Int     = -1
    }
    
    // MARK: Generic empty
    struct emptyState : Codable {
        
    }

    // Build initial state for any game
    static func createGameStateStructure(
        gameType: GameType,
        clientPlayerProfile: Profile,
        matchedPlayerProfile: Profile
    ) -> Codable {
        switch gameType {
        case .none:
            return emptyState()
        case .ghosted:
            return emptyState()
        case .ghostHunter:
            return emptyState()
        case .heartfall:
            return emptyState()
        case .memoryMatch:
            return emptyState()
        case .redFlagRacing:
            return emptyState()
        case .rpgBattle:
            let bossCase = Int.random(in: 0...2)
            let bossId: String = BossType.allCases[bossCase].rawValue
            
            return RPGState(
                playerNames: [clientPlayerProfile.name, matchedPlayerProfile.name],
                bossId: bossId,
                playerTurn: 0,
                playerNum: 1,
                lastPlayerMove: .None,
                playerHPs: [100, 100],
                playerStatuses: [.none, .none],
                playerStatusDurations: [0, 0],
                bossHP: 500,
                bossStatus: .none,
                bossStatusDuration: 0,
                randomSeed: 5678 /*Int.random(in: 0...Int.max)*/,
                playersWon: false,
                myPlayerIndex: 1
            )

        case .ticTacToe:
            return TicTacToeData(
                nameP1: clientPlayerProfile.name,
                nameP2: matchedPlayerProfile.name
            )

        case .wipeTheIck:
            return 0
        }
    }
}
struct GameMessageData: Codable {
    var game_name: GameType
    var game_state: String
    
    init(gameIdentifier: GameType, stateJSON: String) {
        self.game_name = gameIdentifier
        self.game_state = stateJSON
    }
}

/*
struct GameObject : Identifiable {
    
    let id : UUID = UUID()
    let type : GameType
    
}
*/
