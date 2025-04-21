//
//  Unity.swift
//  unhinged app
//
//  Created by Harry Sho on 1/23/25.
//
//  Reference: https://github.com/bdeweygit/unity-swiftui/blob/main/SwiftUIProject/UnitySwiftUI/Unity.swift
//

import Foundation
import UnityFramework

@objc class Unity : UnityFramework {
    
    static let shared = Unity()
    //private let dataBundleId: String = "com.unity3d.framework"
    //private let frameworkPath: String = "/Frameworks/UnityFramework.framework"
    
    private var loaded = false
    private var framework: UnityFramework
    private var nativeCall: NativeCallProtocol
    
    // Expose Unity's UIView while loaded
    var view: UIView? { loaded ? framework.appController().rootView : nil }
    
    private override init(){
        // Load framework and get the singleton instance
        let bundle = Bundle(path: "\(Bundle.main.bundlePath)/Frameworks/UnityFramework.framework")!
        bundle.load()
        framework = bundle.principalClass!.getInstance()!
        
        /* Send our executable's header data to Unity's CrashReporter.
           Using _mh_execute_header might be more correct, but this is broken on
           Xcode 16. See forum discussion: forums.developer.apple.com/forums/thread/760543 */
        let executeHeader = #dsohandle.assumingMemoryBound(to: MachHeader.self)
        framework.setExecuteHeader(executeHeader)

        // Set bundle containing Unity's data folder
        framework.setDataBundleId("com.unity3d.framework")

        // Register native call protocol
        let proxy: NativeCallProtocol = NativeCallProtocol()
        nativeCall = proxy
        FrameworkLibAPI.registerAPIforNativeCalls(nativeCall)
    }

    func start() {
        framework.runEmbedded(withArgc: CommandLine.argc, argv: CommandLine.unsafeArgv, appLaunchOpts: nil)
        loaded = true
        print("Started Unity Instance")
    }
    
    func stop() {
        // docs.unity3d.com/ScriptReference/Application.Unload.html
        framework.unloadApplication()
        loaded = false
        print("Unloaded Unity Instance")
    }
    
}



/*
 //MARK: Callers
 
 //
 if let container = unity.view.flatMap({ UIViewContainer(containee: $0) }) {...}
 
 //start unity with async execution
 Button("Start Unity", systemImage: "play", action: {
    /* Unity startup is slow and must must occur on the
       main thread. Use async dispatch so we can re-render
       with a ProgressView before the UI becomes unresponsive. */
    loading = true
    DispatchQueue.main.async(execute: {
        unity.start()
        loading = false
    })
 })
 */


/*
import Foundation
import UnityFramework

class Unity: UIResponder, UIApplicationDelegate {
    
    static let shared = Unity()
    
    private let dataBundleId: String = "com.unity3d.framework"
    private let frameworkPath: String = "/Frameworks/UnityFramework.framework"
    
    private var ufw: UnityFramework?
    private var hostMainWindow: UIWindow?
    
    private var isInitialized: Bool {
        ufw?.appController() != nil
    }
    
    func show() {
        if isInitialized {
            showWindow()
        } else {
            initWindow()
        }
    }
    
    func setHostMainWindow(_ hostMainWindow: UIWindow?) {
        self.hostMainWindow = hostMainWindow
    }
    
    private func initWindow() {
        if isInitialized {
            showWindow()
            return
        }
        
        guard let ufw = loadUnityFramework() else {
            print("ERROR: Was not able to load Unity")
            return unloadWindow()
        }
        
        self.ufw = ufw
        ufw.setDataBundleId(dataBundleId)
        ufw.register(self)
        ufw.runEmbedded(
            withArgc: CommandLine.argc,
            argv: CommandLine.unsafeArgv,
            appLaunchOpts: nil
        )
    }
    
    private func showWindow() {
        if isInitialized {
            ufw?.showUnityWindow()
        }
    }
    
    private func unloadWindow() {
        if isInitialized {
            ufw?.unloadApplication()
        }
    }
    
    private func loadUnityFramework() -> UnityFramework? {
        let bundlePath: String = Bundle.main.bundlePath + frameworkPath
        
        let bundle = Bundle(path: bundlePath)
        if bundle?.isLoaded == false {
            bundle?.load()
        }
        
        let ufw = bundle?.principalClass?.getInstance()
        if ufw?.appController() == nil {
            let machineHeader = UnsafeMutablePointer<MachHeader>.allocate(capacity: 1)
            machineHeader.pointee = _mh_execute_header
            
            ufw?.setExecuteHeader(machineHeader)
        }
        return ufw
    }
}

extension Unity: UnityFrameworkListener {
    
    func unityDidUnload(_ notification: Notification!) {
        ufw?.unregisterFrameworkListener(self)
        ufw = nil
        hostMainWindow?.makeKeyAndVisible()
    }
}
*/
