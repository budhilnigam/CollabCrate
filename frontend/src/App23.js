import { ref,h } from 'vue';
import { RouterLink, RouterView } from 'vue-router';
import HomeNavBar from './components/HomeNavBar';
import SponsorNavBar from './components/Sponsors/SponsorNavBar';
import InfluencerNavBar from './components/Influencers/InfluencerNavBar';
import './App.css';
export default {
  el:"#app",
  components: {
    RouterLink,
    RouterView,
    HomeNavBar,
    SponsorNavBar,
    InfluencerNavBar,
  },
  setup() {
    const userType = ref('anonymous');
    if (localStorage.getItem('userRole') !== null) {
      userType.value = localStorage.getItem('userRole');
    }

    return {
      userType,
    };
  },
  render() {
    return h('div', { style: 'width:100%;margin:auto' }, [
      this.userType === 'anonymous' ? h(HomeNavBar) : null,
      this.userType === 'sponsor' ? h(SponsorNavBar) : null,
      this.userType === 'influencer' ? h(InfluencerNavBar) : null,
      h(RouterView),
    ]);
  }
};
