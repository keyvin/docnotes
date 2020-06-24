using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Threading;
using System.IO;
namespace SaveMoverTray
{
 
  
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        public static string defaultsPath;
        [STAThread]

        static void Main()
        {
            var appDataPath = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            defaultsPath = Path.Combine(appDataPath, @"savemover\");
            if (!Directory.Exists(defaultsPath))
                Directory.CreateDirectory(defaultsPath);

            GameList games = new GameList();
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1(games));
            games.SaveList();
        }
    }
}
