//Created By Benjamin Steinberg
//Date created: 4/15/2025


using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.SceneManagement;
using System.Collections;
using System.Collections.Generic;

public class SpaghettiDateEscape : MonoBehaviour, IGameStateProvider
{
    [Header("UI Panels")]
    public GameObject startScreen;
    public GameObject winScreen;
    public GameObject loseScreen;
    public TMP_Text timerText;

    [Header("Gameplay")]
    public GameObject player;
    public GameObject enemyPrefab;
    public GameObject bulletPrefab;
    public float enemySpawnRate = 0.05f;
    public float enemySpeed = 4f;
    public float bulletSpeed = 8f;
    public float duration = 20f;
    public AudioSource italianMusic;
    public AudioSource tromboneSFX;

    private bool gameActive = false;
    private float gameTimer;
    private List<GameObject> enemies = new List<GameObject>();

    void Start()
    {
        startScreen.SetActive(true);
        winScreen.SetActive(false);
        loseScreen.SetActive(false);
        player.SetActive(false);
        if (timerText != null) timerText.text = "";
    }

    public void StartGame()
    {
        // Spawn player in center of the screen
        player.transform.position = Vector3.zero;
        startScreen.SetActive(false);
        winScreen.SetActive(false);
        loseScreen.SetActive(false);
        player.SetActive(true);

        if (italianMusic) italianMusic.Play();

        gameActive = true;
        gameTimer = duration;
        if (timerText != null) timerText.text = gameTimer.ToString("F1") + "s";
        StartCoroutine(SpawnEnemies());
        StartCoroutine(FireBulletsMulti());
    }

    void Update()
    {
        if (!gameActive) return;

        Vector3? targetPos = null;
        if (Input.touchCount > 0)
        {
            Touch touch = Input.GetTouch(0);
            targetPos = Camera.main.ScreenToWorldPoint(touch.position);
        }
        else if (Input.GetMouseButton(0))
        {
            targetPos = Camera.main.ScreenToWorldPoint(Input.mousePosition);
        }

        if (targetPos.HasValue)
        {
            Vector3 target = new Vector3(targetPos.Value.x, targetPos.Value.y, 0);
            float speed = 2f; // Player movement speed
            player.transform.position = Vector3.MoveTowards(player.transform.position, target, speed * Time.deltaTime);
        }

        gameTimer -= Time.deltaTime;
        if (timerText != null) timerText.text = Mathf.Max(gameTimer, 0f).ToString("F1") + "s";

        if (gameTimer <= 0)
        {
            StartCoroutine(EndGame());
        }
    }

    IEnumerator SpawnEnemies()
    {
        while (gameActive)
        {
            Vector2 spawnDir = Random.insideUnitCircle.normalized * 6f;
            Vector3 spawnPos = new Vector3(spawnDir.x, spawnDir.y, 0);
            GameObject enemy = Instantiate(enemyPrefab, spawnPos, Quaternion.identity);
            enemies.Add(enemy);
            StartCoroutine(MoveEnemy(enemy));
            yield return new WaitForSeconds(enemySpawnRate);
        }
    }

    IEnumerator MoveEnemy(GameObject enemy)
    {
        while (enemy && gameActive)
        {
            Vector3 dir = (player.transform.position - enemy.transform.position).normalized;
            enemy.transform.position += dir * enemySpeed * Time.deltaTime;

            if (Vector3.Distance(enemy.transform.position, player.transform.position) < 0.5f)
            {
                Destroy(enemy);
                gameActive = false;
                player.SetActive(false);
                foreach (var e in enemies) Destroy(e);
                enemies.Clear();
                if (italianMusic && italianMusic.isPlaying) italianMusic.Stop();
                if (tromboneSFX) tromboneSFX.Play();
                loseScreen.SetActive(true); // You got hit!
                if (timerText != null) timerText.text = "";
            }

            yield return null;
        }
    }

    IEnumerator FireBulletsMulti()
    {
        while (gameActive)
        {
            int bulletCount = 6; // Number of directions to shoot
            for (int i = 0; i < bulletCount; i++)
            {
                float angle = i * Mathf.PI * 2f / bulletCount;
                Vector2 direction = new Vector2(Mathf.Cos(angle), Mathf.Sin(angle));
                GameObject bullet = Instantiate(bulletPrefab, player.transform.position, Quaternion.identity);
                StartCoroutine(MoveBullet(bullet, direction));
            }
            yield return new WaitForSeconds(2.0f);
        }
    }

    IEnumerator MoveBullet(GameObject bullet, Vector2 direction)
    {
        float lifetime = 0.4f;
        float elapsedTime = 0f;

        while (bullet && gameActive && elapsedTime < lifetime)
        {
            bullet.transform.Translate(direction * bulletSpeed * Time.deltaTime);
            elapsedTime += Time.deltaTime;

            for (int i = enemies.Count - 1; i >= 0; i--)
            {
                GameObject enemy = enemies[i];
                if (enemy && Vector3.Distance(bullet.transform.position, enemy.transform.position) < 0.5f)
                {
                    Destroy(enemy);
                    enemies.RemoveAt(i);
                    Destroy(bullet);
                    yield break;
                }
            }

            yield return null;
        }

        if (bullet) Destroy(bullet);
    }



    IEnumerator EndGame()
    {
        if (italianMusic && italianMusic.isPlaying) italianMusic.Stop();
        gameActive = false;
        player.SetActive(false);
        foreach (var e in enemies) Destroy(e);
        enemies.Clear();
        if (timerText != null) timerText.text = "";
        yield return new WaitForSeconds(0.5f);
        winScreen.SetActive(true);
    }

    public void RestartGame()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }

    public string GetGameStateJSON()
    {
        return "{\"result\": true}";
    }
}
