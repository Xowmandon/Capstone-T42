//
//  AccountConfigSheet.swift
//  unhinged app
//
//  Created by Harry Sho on 2/20/25.
//

import SwiftUI
import Foundation

struct AccountConfigSheet : View {
    @EnvironmentObject var appModel : AppModel
    var body : some View {
        NavigationStack{
            VStack{
                HStack{
                    
                    BackButton()
                    Spacer()
                    
                }
                .padding(.top)
                
                //Build Profile
                NavigationLink(destination: BuildProfileView(profile: appModel.profile)) {
                    HStack{
                        
                        //Avatar
                        Circle()
                            .frame(maxHeight: 100)
                        Text("\(AccountData.shared.profile.name)'s Profile")
                    }
                    .padding()
                    .background{
                        CardBackground()
                    }
                }
                
                //Match Making Preferences
                NavigationLink(destination: MatchPreferencesView()){
                    HStack{
                        Image(systemName: "slider.horizontal.2.square")
                        Text("Matchmaking Preferences")
                    }
                    .padding()
                    .background{
                        CardBackground()
                    }
                }
                
                //Account
                VStack{
                    Text("Logged in as: <name>")
                    HStack{
                        Image(systemName: "person.fill.xmark")
                            .foregroundStyle(.red)
                        Text("Logout")
                    }
                }
                .padding()
                .background {
                    CardBackground()
                }
                Spacer()
            }
            .frame(alignment: .leading)
        }
        .navigationBarBackButtonHidden()
    }
}

#Preview{
    
    AccountConfigSheet()
    
}
