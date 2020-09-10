using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.Text.RegularExpressions;


public class Post : MonoBehaviour
{
    public LoadAndDisplayImages loadAndDisplayImages;

    [System.Serializable]
    public class ocr
    {
        public string data;
    }

    //  public LoadAndDisplayImages ladi;
    
    
    
    public void PostData(string st)
    {
        st=Regex.Replace(st, @"\t\n\r", "").Replace('[',' ').Replace(']',' ');
         
        ocr o = new ocr();
        o.data = st;

        string json = JsonUtility.ToJson(o);
        StartCoroutine(PostRequest("http://localhost:5000/list_add", json,st));
    }

    IEnumerator PostRequest(string url, string json,string ocr)
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
            loadAndDisplayImages.seperateUrlsAndDownload(uwr.downloadHandler.text, ocr);
        }
    }
}
