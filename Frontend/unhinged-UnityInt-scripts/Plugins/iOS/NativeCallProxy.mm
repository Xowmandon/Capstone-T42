//harry aguinaldo 04/21/2025

#import <Foundation/Foundation.h>
#import "NativeCallProxy.h"


@implementation FrameworkLibAPI

id<NativeCallsProtocol> api = NULL;
+(void) registerAPIforNativeCalls:(id<NativeCallsProtocol>) aApi
{
    api = aApi;
}

@end


extern "C" {
    void showHostMainWindow(const char* color) { return [api showHostMainWindow:[NSString stringWithUTF8String:color]]; }

    void sendGameResultToHost(bool win) {
        [api sendGameResult:[NSNumber numberWithBool:win]];
    }

    void sendGameSaveDataToHost(const char* json) {
        [api sendGameSaveData:[NSString stringWithUTF8String:json]];
    }

    void didFinishLoadingInstance(){
        [api didFinishLoadingInstance];
    }
}

