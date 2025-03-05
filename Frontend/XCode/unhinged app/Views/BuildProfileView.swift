//
//  BuildProfileView.swift
//  unhinged app
//
//  Created by Harry Sho on 2/20/25.
//

import Foundation
import SwiftUI
import PhotosUI

struct BuildProfileView: View {
    
    //TODO: confirm changes upon dismiss
    //TODO: use .overlay for edit button
    
    @State var profile : Profile
    var theme : Theme = Theme.shared
    var editButtonImage : String = "pencil.circle.fill"
    
    @State var showAddObjectSheet : Bool = false
    @State var showAvatarBuilderSheet : Bool = false // TODO: Avatar Builder
    @State var showEditProfileCardSheet : Bool = false // TODO: Image Picker
    @State var showAttributeCreatorSheet : Bool = false  //TODO: Attribute builder
    
    @State var biographyText : String = ""
    @State var profileImageItem : PhotosPickerItem?
    @State var profileImage : Image = Image(systemName: "person.fill")
    /*
    
    @State var name : String
    @State var attributes : [Attribute]
    var prompts : [PromptItem]
    */
    @FocusState private var isEditingBiography: Bool
    /*
    init(){
        //Initialize variables with existing profile data
        _name = State(initialValue: (profile.name))
        _biography = State(initialValue: profile.biography ?? "No Bio written yet")
        _attributes = State(initialValue: profile.attributes)
        prompts = []
    }
     */
    public var body: some View {
        ZStack {
            
            // Profile Content
            ScrollView{
                
                Text("My Profile")
                    .font(Theme.titleFont)
                
                //Avatar Customization
                Text("Avatar")
                    .font(Theme.headerFont)
                Circle()
                    .foregroundStyle(Color.blue)
                    .frame(maxWidth: 100)
                    .overlay{
                        Image(systemName: "pencil.circle.fill")
                            .font(.system(.title))
                            .frame(minWidth: 100, minHeight: 100, alignment: .topTrailing)
                    }
            
                ZStack(alignment: .topTrailing) {
                    ProfileCard(profileImage: profileImage, name: "\(profile.name)", age: 2)
                        .padding(.horizontal)
                        .frame(minHeight: 400)
                    
                    PhotosPicker(selection: $profileImageItem,
                                 matching: .images,
                                 photoLibrary: .shared()) {
                        Image(systemName: "pencil.circle.fill")
                            .symbolRenderingMode(.multicolor)
                            .font(.system(size: 30))
                            .foregroundColor(.accentColor)
                    }
                    .buttonStyle(.borderless)
                     
                }
                
                // Basic Info (Attributes?)
                
                ZStack(alignment:.topTrailing) {
                    VStack (spacing: 5){
                        ForEach(profile.attributes, id: \.self) { attribute in
                            HStack{
                                Image(systemName: attribute.symbolName)
                                Text(attribute.customName)
                                    .font(Theme.bodyFont)
                            }
                        }
                    }
                    .padding()
                    .frame(maxWidth:.infinity)
                    .background{
                        CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                    }
                    .padding()
                }
                
                // Biography
                VStack{
                    HStack{
                        Text("About Me!")
                            .font(Theme.headerFont)
                            .padding(.top)
                            .padding(.horizontal)
                        Spacer()
                        
                        Button(action: {
                            isEditingBiography.toggle()
                        }, label: {
                            Image(systemName: editButtonImage).padding(.horizontal).font(.title2)
                        })
                        
                    }
                    TextEditor(text:$biographyText)
                        .focused($isEditingBiography)
                        .font(Theme.bodyFont)
                        .padding()
                        .frame(minHeight: 10)
                        .onAppear{
                            biographyText = profile.biography ?? "Create a Biography..."
                        }
                        
                }
                .padding()
                .background{
                    CardBackground(borderColor: theme.cardBorderColor, innerColor: theme.cardInnerColor)
                }
                .padding(.horizontal)
                
                
                //TODO: Image Gallery
                //Prompts
                ForEach(profile.prompts ?? []){prompt in
                    PromptView(prompt: prompt)
                        .padding()
                }
                Spacer()
                    .padding(.vertical, 60)
            }
            
            //Overlay
            VStack {
                HStack{
                    BackButton()
                    Spacer()
                }
                Spacer()
                if !isEditingBiography {
                    Button(action: {showAddObjectSheet.toggle()}){
                        Image(systemName: "plus")
                            .imageScale(.large)
                            .symbolRenderingMode(.monochrome)
                            .foregroundStyle(.green)
                            .font(.system(.title, weight: .black))
                            .padding()
                            .background{
                                Circle()
                                    .fill(.ultraThickMaterial)
                                    .shadow(radius: 5)
                            }
                    }
                }
            }
        }
        .navigationBarBackButtonHidden()
        .onChange(of: profileImageItem) {
                    Task {
                        if let imgData = try? await profileImageItem?.loadTransferable(type: Data.self) {
                            let uiImg = UIImage(data: imgData)
                            profileImage = Image(uiImage: uiImg!)
                        } else {
                            print("Failed")
                        }
                    }
                }
        .toolbar {
            ToolbarItem(placement: .keyboard) {
                HStack{
                    Spacer()
                    Button("Done") {
                        isEditingBiography = false // Dismiss keyboard
                    }
                }
            }
        }
        //Add Object Sheet
        .sheet(isPresented: $showAddObjectSheet){
            VStack {
                Text("Customize Your Profile")
                    .font(Theme.headerFont)
                    .padding()
                VStack {
                    HStack {
                        Text("Add A Prompt")
                            .font(Theme.headerFont)
                            .padding()
                        Spacer()
                        Image(systemName: "plus.app")
                            .imageScale(.large)
                            .symbolRenderingMode(.hierarchical)
                            .padding()
                    }
                    Text("Keep your matches guessing with a custom prompt - be creative!")
                        .font(Theme.bodyFont)
                        .padding()
                    PromptView(prompt: PromptItem.examplePrompt)
                        .padding()
                }
                VStack {
                    HStack {
                        Text("Add A Photo")
                            .padding()
                            .font(.system(.title3, weight: .medium))
                        Spacer()
                        Image(systemName: "plus.app")
                            .imageScale(.large)
                            .symbolRenderingMode(.hierarchical)
                            .padding()
                    }
                    RoundedRectangle(cornerRadius: 10, style: .continuous)
                        .fill(Color(.secondarySystemBackground))
                        .frame(maxWidth: .infinity, maxHeight: 200)
                        .clipped()
                        .padding(20)
                        .overlay {
                            VStack {
                                HStack {
                                    Text("My Favorite Place")
                                        .font(.headline)
                                        .foregroundStyle(.primary)
                                        .padding(.horizontal, 40)
                                    Spacer()
                                }
                                Image("myImage")
                                    .renderingMode(.original)
                                    .resizable()
                                    .aspectRatio(contentMode: .fit)
                                    .frame(maxWidth: .infinity, maxHeight: 130)
                                    .clipped()
                                    .overlay {
                                        Group {
                                            
                                        }
                                    }
                                    .mask {
                                        RoundedRectangle(cornerRadius: 20, style: .continuous)
                                            .clipped()
                                    }
                            }
                        }
                }
            }
            
        }
        //Profile Card Sheet
        .sheet(isPresented: $showEditProfileCardSheet){
            
        }
    }
    
    func saveProfile() {
        AccountData.shared.setProfile(self.profile)
        
        //TODO: Push new profile data to server
    }
}

private extension PhotosPickerItem {
    var identifier: String {
        guard let identifier = itemIdentifier else {
            fatalError("The photos picker lacks a photo library.")
        }
        return identifier
    }
}

#Preview{
    
    let profile = AccountData.shared.profile
    BuildProfileView(profile: profile)
    
}
