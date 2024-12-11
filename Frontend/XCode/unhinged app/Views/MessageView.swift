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
import SwiftData

struct MessageView : View {
    
    let profile : Profile
    
    var body: some View {
        
        Text("a")
        
    }
    
    private func sendMesage(){
        
        // push message
        
        APIClient.shared
        
    }
    
    private func fetchMessages(){
        
        //
        
        APIClient.shared
        
    }
    
}


#Preview {
    
    MessageView(profile: Profile())
    
}

