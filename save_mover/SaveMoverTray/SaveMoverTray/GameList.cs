using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;


namespace SaveMoverTray
{
    public class GameList
    {
        List<Game> gameList;
        string saveDirectory { get; }
        public GameList()
        {
            gameList = new List<Game>();
        }
        public void AddGame(Game ToAdd)
        {
            if (ToAdd.AutoCopy)
            {
                ToAdd.StartWatch();
            }
            gameList.Add(ToAdd);

        }

        public bool LoadList(string fileName = "gamelist.json")
        {
            List<Game> failList = new List<Game>();
            string text = "";
            if (System.IO.File.Exists("gamelist.json"))
            {
                text = System.IO.File.ReadAllText("gamelist.json");

                gameList = JsonConvert.DeserializeObject<List<Game>>(text);
                foreach (var a in gameList)
                {
                    if (a.AutoCopy && !a.StartWatch())
                    {
                        failList.Add(a);
                    }
                }
                foreach (var tor in failList)
                {
                    gameList.Remove(tor);
                }
            }
            return true;
        }
        
        public List<string> GetGames()
        {
            List<string> names = new List<string>();
            foreach (var game in gameList)
            {
                names.Add(game.Name);
            }
            return names;
        }
        public bool SaveList(String fname="gamelist.json")
        {
            string json = JsonConvert.SerializeObject(gameList) ;
            System.IO.File.WriteAllText(fname, json);

            return true;
        }
        //coupling this saves a lot of work.
        public string DoAutoCopy()
        {
            string result = "";
            foreach (var a in gameList)
            {

                if (a.Updated && a.Copying == false)
                {
                    TimeSpan diff = DateTime.Now - a.LastUpdatEvent;
                    if (diff.TotalSeconds > 3)
                    {
                        result = result + a.Name + " Updated. Starting Copy\r\n";
                        a.Copying = true;
                        a.makeZip();
                    }
                }
                if (a.Updated && a.Copying == true && a.Finished == true)
                {
                    //log to parent....
                    a.Updated = false;
                    a.Copying = false;
                    a.Finished = false;
                    result = result + a.Name + " Finished Copying\r\n";

                }

            }
          
            if (result != "")
                System.Console.WriteLine(result);
            return result;
        }
        public bool NameExists(string name)
        {
            foreach (var game in gameList)
            {
                if (game.Name == name)
                {
                    return true;
                }
            }
            return false;
        }
        public bool PathExists(string path)
        {
            foreach (var game in gameList)
            {
                if (game.GameDir == path)
                {
                    return true;
                }
            }
            return false;
            
        }

       
        
    }
}
