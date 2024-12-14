using System.Collections;
using UnityEngine;

public static class Lerpers
{
    public static float FloatLerp(float a, float b, float t) => a + ( b - a ) * t;

    public static float InQuad(float t) => t * t;

    public static float Flip(float t) => 1 - t;

    public static float OutQuad(float t) => Flip(InQuad(Flip( t )));

    public static float InOutQuad(float t) => FloatLerp( InQuad( t ), OutQuad( t ), t );

    public static float CustomEase(float t, float a, float b)
    {
        float c = 1 - a - b;
        return ( a * t * t * t ) + ( b * t * t ) + ( c * t );
    }

    public static float LinearEase(float t) => CustomEase(t, 0, 0);

    public static float InBack(float t) => CustomEase(t, 1.5f, 0);

    public static float OutBack(float t) => CustomEase(t, 1.25f, -4);

    public static Vector2 PositionLerp2d(Vector2 start_value, Vector2 end_value, float t)
    {
        t = Mathf.Clamp01(t); //assures that the given parameter "t" is between 0 and 1
    
        return new Vector2(
            start_value.x + (end_value.x - start_value.x) * t,
            start_value.y + (end_value.y - start_value.y) * t
        );
    }

    public static Vector3 Vector3Lerp(Vector3 start_value, Vector3 end_value, float t)
    {
        t = Mathf.Clamp01(t); //assures that the given parameter "t" is between 0 and 1
    
        return new Vector3(
            start_value.x + (end_value.x - start_value.x) * t,
            start_value.y + (end_value.y - start_value.y) * t,
            start_value.z + (end_value.z - start_value.z) * t
        );
    }

    public static IEnumerator LerpTransform(Transform transform, Vector3 target, float duration)
    {
        float time = 0;
        Vector3 startPosition = transform.position;
        while (time < duration)
        {
            transform.position = Vector3Lerp(startPosition, target, time / duration);
            time += Time.deltaTime;
            yield return null;
        }
        transform.position = target;
    }
}