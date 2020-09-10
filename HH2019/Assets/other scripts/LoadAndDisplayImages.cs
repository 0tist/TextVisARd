using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class LoadAndDisplayImages : MonoBehaviour
{
    public Post Post;
    public GameObject quad;
    public setText setText;
    public string urls;

    public void seperateUrlsAndDownload(string urls,string ocrtext)
    {
        setText.loadText(ocrtext);
        
        string[] brk = {"%42069420%"};
        string[] arr = urls.Split(brk, System.StringSplitOptions.None);

        if (arr[0].Length > 0)
            setText.loadSummary(arr[0]);

        Debug.Log(arr[1]);
        if (arr[1].Length > 0) { 
            string[] MediaUrls = arr[1].Split('|');
            StartCoroutine(DownloadImage(MediaUrls));
        }


    }
 
    IEnumerator DownloadImage(string[] MediaUrls)
    {
        List<Texture> textures = new List<Texture>();

        for (int i = 0; i < MediaUrls.Length - 1; i++)
        {
            Debug.Log("here");
            Debug.Log("url->" + MediaUrls[i]);
            string MediaUrl = MediaUrls[i];
            
            UnityWebRequest request = UnityWebRequestTexture.GetTexture(MediaUrl);
            yield return request.SendWebRequest();
            if (request.isNetworkError || request.isHttpError)
                Debug.Log(request.error);
            else
                textures.Add(((DownloadHandlerTexture)request.downloadHandler).texture);
        }

        for (int i = 0; i < textures.Count; i++)
        {
            quad.GetComponent<Renderer>().material.mainTexture = textures[i];

            yield return new WaitForSeconds(3);

            if (i == textures.Count - 1)
            {
                i = -1;
            }

        }
    }

}
