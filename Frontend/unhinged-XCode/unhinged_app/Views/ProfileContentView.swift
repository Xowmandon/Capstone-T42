//
//  ProfileContentView.swift
//  
//
//  Created by Harry Sho on 4/25/25.
//
import SwiftUI

struct ProfileContentView : View{
    
    let theme = Theme.shared
    
    var currentProfile : Profile?
    
    //TODO: change values with profile instance
    @ViewBuilder
    func ProfileCard(profile: Profile) -> some View {
        
        ZStack {
            //Profile Image
            VStack (spacing: 0) {
                GeometryReader { geometry in
                    profile.image
                        .resizable()
                        .scaledToFill()
                        .frame(width: geometry.size.width, height: geometry.size.height)
                        .mask(Rectangle())
                        .clipped()
                }
                .padding(5)
                .background{
                    CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                }
                
                //Profile Information
                VStack {
                    HStack(spacing: 20){
                        Text(profile.name)
                            .font(Theme.titleFont)
                            //.font(.system(.largeTitle, weight: .bold))
                            //.offset(x: -2)
                        Spacer()
                        Text(String(profile.age))
                            .font(Theme.titleFont)
                    }
                }
                .padding(.horizontal, 30)
                .padding(.vertical, 30)
                .background{
                    CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                }
            }
        }
    }
    
    @ViewBuilder
    func AttributeRow(attribute: Attribute) -> some View {
        HStack{
            Image(systemName: attribute.symbolName)
            Text(attribute.customName)
                .font(Theme.bodyFont)
        }
    }
    
    @ViewBuilder
    func LocationSection (city: String , state: String) -> some View {
        VStack {
            HStack {
                Image(systemName: "mappin")
                    .foregroundStyle(.secondary)
                Text("Location")
                    .font(Theme.headerFont)
                Spacer()
            }
            VStack (alignment: .leading){
                HStack {
                    Text("City:")
                    Text(city)
                    Spacer()
                }
                HStack{
                    Text("State:")
                    Text(state)
                    Spacer()
                }
            }
            .padding(.leading)
        }
        .padding()
        .font(Theme.bodyFont)
        .background{
            CardBackground()
        }
        
    }
    
    @ViewBuilder
    func AboutMeSection(bio: String) -> some View {
        VStack{
            HStack{
                Text("About Me!")
                    .font(Theme.headerFont)
                    .padding(.top)
                    .padding(.horizontal)
                Spacer()
            }
            Text("\(bio)")
                .font(Theme.bodyFont)
                .padding()
        }
        .padding()
        .background{
            CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
        }
    }
    
    
    var body: some View {
        VStack (spacing: 5){
            ProfileCard(profile: currentProfile ?? Profile(name: "NULL PROFILE"))
                .frame(minHeight: 400)
            
            // Attribute Section
            /*
             VStack (spacing: 5){
             ForEach(currentProfile!.attributes, id: \.self) { attribute in
             AttributeRow(attribute:attribute)
             }
             }
             .padding()
             .frame(maxWidth:.infinity)
             .background{
             CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
             }
             .padding()
             */
            // MARK: Location
            
            LocationSection(city: currentProfile?.city ?? "No City", state: currentProfile?.state.fullName ?? "No State")
            
            // MARK: Biography Section
            AboutMeSection(bio: currentProfile?.biography ?? "No bio provided")
            
            // MARK: Gallery
            
            if let gallery = currentProfile?.gallery {
                
                ForEach(gallery) { card in
                    GalleryCard(image: card.image, title: card.title, description: card.description)
                }
                
            }
            
            // MARK: Prompts
            
            if let prompts = currentProfile?.prompts {
                ForEach(prompts) { prompt in
                    PromptView(prompt: prompt)
                }
            }
        }
        .padding(.horizontal)
    }
}
