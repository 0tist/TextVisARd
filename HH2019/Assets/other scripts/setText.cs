using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class setText : MonoBehaviour
{
    public TextMeshPro tM;
    public TextMeshPro tS;

    public void loadText(string ocrtext)
    {
        tM.GetComponent<TextMeshPro>().text = ocrtext;
    }

    public void changePageNext()
    {
        tM.pageToDisplay++ ;
    }

    public void changePagePrev()
    {
        tM.pageToDisplay--;
    }

    public void loadSummary(string summary)
    {
        tS.GetComponent<TextMeshPro>().text = summary;
    }

    public void changePageNextS()
    {
        tS.pageToDisplay++;
    }

    public void changePagePrevS()
    {
        tS.pageToDisplay--;
    }
}
