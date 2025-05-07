// [!] important set UnityFramework in Target Membership for this file
// [!]           and set Public header visibility

//harry aguinaldo 04/21/2025

#import <Foundation/Foundation.h>

// NativeCallsProtocol defines protocol with methods you want to be called from managed
// methods implemented on swift layer
@protocol NativeCallsProtocol
@required
- (void) showHostMainWindow:(NSString*)color;
- (void) didFinishLoadingInstance;
- (void)sendGameResult:(NSNumber*)win;
- (void)sendGameSaveData:(NSString*)gameJSON;
// other methods
@end

__attribute__ ((visibility("default")))
@interface FrameworkLibAPI : NSObject
// call it any time after UnityFrameworkLoad to set object implementing NativeCallsProtocol methods
+(void) registerAPIforNativeCalls:(id<NativeCallsProtocol>) aApi;

@end
