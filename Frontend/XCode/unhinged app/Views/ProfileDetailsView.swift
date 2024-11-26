//
//  ProfileDetailsView.swift
//  unhinged app
//
//  Created by Harry Sho on 11/7/24.


import SwiftUI


struct ProfileDetailsView : View {
    
    var body : some View {
        
        ZStack{
            VStack{
                
                Image("stockPhoto")
                    .resizable()
                    .scaledToFill()
                    .clipped()
                    .frame(width: .infinity, height: 400)
                    .mask{
                        
                        RoundedRectangle(cornerRadius: 20)
                            .frame(width: 400, height: 400)
                        
                        
                    }
                Spacer()
                
            }
            .ignoresSafeArea(.container)
            
            ScrollView{
            
                VStack{
                    HStack{
                        
                        Text("John Doe")
                            .font(.title)
                            .foregroundStyle(.primary)
                        Text("21")
                            .font(.title2)
                        
                    }
                    .frame(alignment:.leading)
                    
                }
                
            }
            .frame(alignment: .leading)
            
        }
        .toolbarBackgroundVisibility(.hidden, for: .navigationBar)
        .toolbar{
            ToolbarItem(placement: .topBarLeading){
                
                BackButton()
                
            }
            
        }
        
    }
    
}

#Preview {
    NavigationStack{
        ProfileDetailsView()
    }
}
