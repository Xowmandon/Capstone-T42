//Author: Benjamin Steinberg
//debugger

using UnityEngine;

public class RawCanvasRendererScanner : MonoBehaviour
{
    void LateUpdate()
    {
        var renderers = FindObjectsOfType<CanvasRenderer>();
        foreach (var cr in renderers)
        {
            if (cr == null || !cr.gameObject.activeInHierarchy) continue;

            var t = cr.transform;
            Vector3 pos = t.localPosition;
            Vector3 scale = t.localScale;

            if (float.IsNaN(pos.x) || float.IsInfinity(pos.x) ||
                float.IsNaN(scale.x) || float.IsInfinity(scale.x))
            {
                Debug.LogError($"CanvasRenderer on {cr.gameObject.name} has invalid transform!\n" +
                               $"Position: {pos}, Scale: {scale}", cr.gameObject);
                return;
            }

            // Log normally just to confirm things are scanning
            Debug.Log($"[CR Scan] {cr.gameObject.name} Pos={pos}, Scale={scale}");
        }
    }
}
