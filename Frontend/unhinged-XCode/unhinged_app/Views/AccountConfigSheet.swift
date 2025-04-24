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
            HStack{
                
                BackButton()
                Spacer()
                Text("My Account")
                    .font(Theme.titleFont)
                Spacer()
                
            }
            .padding()
            List{
                
                //Build Profile
                NavigationLink(destination: BuildProfileView(isFirstTimeCreation: false)) {
                    HStack{
                        
                        //Avatar
                        appModel.profile.image
                            .resizable()
                            .scaledToFit()
                            .mask(Circle())
                            .frame(maxHeight: 100)
                        Spacer()
                        Text("\(AccountData.shared.fullName)")
                            .font(Theme.headerFont)
                        Spacer()
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
                            .font(Theme.bodyFont)
                        Spacer()
                    }
                    .padding()
                    .background{
                        CardBackground()
                    }
                }
                
                //Account
                HStack{
                    VStack{
                        
                        HStack{
                            Image(systemName: "person.fill.xmark")
                                .foregroundStyle(.red)
                            Text("Logout")
                                .font(Theme.bodyFont)
                                .foregroundStyle(.red)
                        }
                    }
                    Spacer()
                }
                .padding()
                .background {
                    CardBackground()
                }
            }
            .frame(alignment: .leading)
            .scrollContentBackground(.hidden)
        }
        .onAppear{
            Task {
                await appModel.getClientUserProfile()
            }
        }
        .navigationBarBackButtonHidden()
    }
}

#Preview{
    
    AccountConfigSheet()
        .environmentObject(AppModel())
    
}
