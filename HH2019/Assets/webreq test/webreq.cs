using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;

public class webreq : MonoBehaviour
{
    public const string URL = "link?filepath=";
    public string file_path;
    public Text responseText;

    public void request()
    {
        WWW request = new WWW(URL+file_path);
        StartCoroutine(onResponse(request));
    }

    IEnumerator onResponse(WWW req)
    {
        yield return req;
        responseText.text = req.text;
    }
}
