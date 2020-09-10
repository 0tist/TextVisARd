using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;


public class test : MonoBehaviour
{
    

    [System.Serializable]
    public class ocr
    {
        public string data;
    }

    //  public LoadAndDisplayImages ladi;
    public string ptr;
    public string urls;


    private void Start()
    {
        PostData();
    }

    public void PostData( )
    {
        string st = ptr;
        st = st.Replace("\\n", " ").Replace('[', ' ').Replace(']', ' ');

        ocr o = new ocr();
        o.data = st;

        string json = JsonUtility.ToJson(o);
        StartCoroutine(PostRequest("http://localhost:5000/list_add", json));
    }

    IEnumerator PostRequest(string url, string json)
    {
        var uwr = new UnityWebRequest(url, "POST");
        byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(json);
        uwr.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
        uwr.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
        uwr.SetRequestHeader("Content-Type", "application/json");

        //Send the request then wait here until it returns
        yield return uwr.SendWebRequest();

        if (uwr.isNetworkError)
        {
            Debug.Log("Error While Sending: " + uwr.error);
        }
        else
        {
            Debug.Log("Received: " + uwr.downloadHandler.text);
            urls = uwr.downloadHandler.text;
            Debug.Log("recieved this" + urls);
            seperateUrlsAndDownload(urls);
        }
    }



    public GameObject quad;



    void seperateUrlsAndDownload(string urls)
    {
        string[] brk = {"%42069420%"};
        string[] arr = urls.Split(brk, System.StringSplitOptions.None);
         
        if (arr[1].Length > 0)
        {
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
