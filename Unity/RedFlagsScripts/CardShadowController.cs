using UnityEngine;

public class CardShadowController : MonoBehaviour
{
    [SerializeField] private Transform shadowTransform;
    [SerializeField] private Vector2 shadowOffset = new(0.2f, -0.2f);

    private Vector3 TargetShadowPos;

    private bool isShadowShown = false;
    private bool isShadowHidden = true;

    private void Update()
    {
        if(transform.GetChild(0).localScale.x > 1 && !isShadowShown)
        {
            OffsetShadow();
        }
        if(transform.GetChild(0).localScale.x < 1.2f && !isShadowHidden)
        {
            HideShadow();
        }
    }

    private void OffsetShadow()
    {
        TargetShadowPos = new(transform.position.x + shadowOffset.x, transform.position.y + shadowOffset.y, 0.1f);
        shadowTransform.position = Lerpers.Vector3Lerp(shadowTransform.position, TargetShadowPos, Lerpers.OutQuad(0.2f));
        isShadowHidden = false;
        isShadowShown = true;
    }

    private void HideShadow()
    {
        Vector3 targetPos = new(transform.position.x, transform.position.y, 0.1f);
        shadowTransform.position = Lerpers.Vector3Lerp(shadowTransform.position, targetPos, Lerpers.OutQuad(0.2f));
        isShadowHidden = true;
        isShadowShown = false;
    }
}
