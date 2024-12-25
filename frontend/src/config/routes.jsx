import { Home as HomeIcon, Folder as FolderIcon, SmartToy as SmartToyIcon, Diamond as DiamondIcon, PhotoLibrary as PhotoLibraryIcon } from '@mui/icons-material';

const Routes = [
  {
    path: '/',
    name: 'Home',
    icon: HomeIcon
  },
  {
    path: '/file-manager',
    name: 'File Manager',
    icon: FolderIcon
  },
  {
    path: '/gallery',
    name: 'Gallery',
    icon: PhotoLibraryIcon
  },
  {
    path: '/the-oracle-gpt',
    name: 'The Oracle GPT',
    icon: SmartToyIcon
  },
  {
    path: '/prism',
    name: 'Prism',
    icon: DiamondIcon
  }
];

export default Routes;
