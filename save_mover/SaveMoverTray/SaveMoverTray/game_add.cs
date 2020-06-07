using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Security.Permissions;
using System.IO.Compression;


namespace SaveMoverTray
{
    public class Game
    {
        public string Name { get; set; }
        public string GameDir { get; set; }
        public bool AutoCopy { get; set;}
        public bool OverWrite { get; set; }
        public bool Updated { get; set; }
        public bool Copying { get; set; }
        public bool Finished { get; set; }
        
        public DateTime LastUpdatEvent { get; set; }
        static public int DelaySeconds { get; set; }
        private FileSystemWatcher watcher;

        public Game()
        {
            Updated = false;
            Copying = false;
        }
 

        public bool StartWatch()
        {

            try
            {
                string fileName = "";
                string directory = "";
                watcher = new FileSystemWatcher();
                FileAttributes attr = File.GetAttributes(GameDir);
                bool isFile = false;

                if ((attr & FileAttributes.Directory) == FileAttributes.Directory)
                {
                    isFile = false;
                    fileName = "*";
                    directory = GameDir;

                }
                else
                {
                    fileName = Path.GetFileName(GameDir);
                    directory = Path.GetDirectoryName(GameDir);
                    isFile = true;
                }

                watcher.Path = directory;

                // Watch for changes in LastAccess and LastWrite times, and
                // the renaming of files or directories.
                watcher.NotifyFilter = watcher.NotifyFilter = NotifyFilters.Attributes |
                NotifyFilters.CreationTime |
                NotifyFilters.FileName |
                NotifyFilters.LastAccess |
                NotifyFilters.LastWrite |
                NotifyFilters.Size |
                NotifyFilters.Security;


                // Only watch text files.
                
                watcher.Filter = fileName;

                // Add event handlers.
                watcher.Changed += OnChanged;
                watcher.Created += OnChanged;
                watcher.Deleted += OnChanged;
                watcher.Renamed += OnRename;

                // Begin watching.
                watcher.EnableRaisingEvents = true;
            }
            catch(Exception e)
            {
                return false;
            }


            return true;

        }

        //todo - log problems.
        public Game(string name, string dir, bool acopy)
        {
            AutoCopy = acopy;
            Updated = false;
            Copying = false;
            Finished = false;
            

            //detect whether its a directory or file            
            if (Directory.Exists(dir) || File.Exists(dir))
            {
                Name = name;
                GameDir = dir;

            }
            else
            {
                return;
            }
            if (AutoCopy)
                StartWatch();
        }

        public void OnChanged(object source, FileSystemEventArgs e)
        {
            LastUpdatEvent = DateTime.Now;
            Updated = true;
            Copying = false;
            System.Console.WriteLine("Updated");
        }

        public void OnRename(object source, RenamedEventArgs e)
        {
            System.Console.WriteLine("Renamed");
            LastUpdatEvent = DateTime.Now;
            Updated = true;
            //Updated = true;
        }

        public async Task<bool> makeZip()
        {
            Finished = false;
            if (File.Exists("c:\\saves\\" + Name + ".zip"))
            {
                File.Delete("c:\\saves\\" + Name + ".zip");
            }
            await Task.Run(() => ZipFile.CreateFromDirectory(GameDir, "c:\\saves\\" + Name + ".zip"));            
            
            Finished = true;
            System.Console.WriteLine("Made zip");
            return true;
        }
    }

}
