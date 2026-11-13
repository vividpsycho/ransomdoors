using System;
using System.Windows;
using System.Windows.Media;
using XamlAnimatedGif;

namespace rans0m
{
    public partial class TauntWindow : Window
    {
        private bool _closed;

        private const string TenorGif = "https://media1.tenor.com/m/SpwFCUCPpiYAAAAd/jx1dx1-ihasafacelulz.gif";

        public TauntWindow()
        {
            InitializeComponent();
            Closed += (_, _) => _closed = true;
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            Global.HideSystemMenu(this);
            Title = "JX1DX1";

            // Taunt popups are visual only. Voice lines play once from the main ransom window.
            Width = 420;
            Height = 180;
            Background = new ImageBrush(Global.tauntImages[Global.rng.Next(Global.tauntImages.Count)])
            {
                Stretch = Stretch.UniformToFill,
                Opacity = 0.35
            };

            try
            {
                AnimationBehavior.SetSourceUri(tauntImage, new Uri(TenorGif));
            }
            catch
            {
                tauntImage.Source = Global.tauntImages[Global.rng.Next(Global.tauntImages.Count)];
            }

            Global.RandomPosWindow(this);
            Global.GlitchIdle(this);
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