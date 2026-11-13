using System;
using System.Windows;

namespace rans0m
{
    public partial class TauntWindow : Window
    {
        private bool _closed;

        public TauntWindow()
        {
            InitializeComponent();
            Closed += (_, _) => { _closed = true; Global.ReleaseTauntWindow(); };
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            Global.HideSystemMenu(this);
            Title = "JX1DX1";
            NoliVoiceLines.TryPlayRandom(this);

            // Exactly one visual per popup: either one supplied still or the supplied GIF.
            Width = 420;
            Height = 240;
            if (Global.rng.Next(2) == 0)
            {
                tauntImage.Source = Global.tauntImages[Global.rng.Next(Global.tauntImages.Count)];
            }
            else
            {
                XamlAnimatedGif.AnimationBehavior.SetSourceUri(
                    tauntImage,
                    new Uri("pack://application:,,,/Assets/Taunts/jx1dx1.gif"));
            }

            Global.RandomPosWindow(this);
            _ = CloseAfterDelayAsync();
        }

        private async Task CloseAfterDelayAsync()
        {
            await Task.Delay(Global.rng.Next(3500, 10001));
            if (_closed) return;
            Close();
        }
    }
}