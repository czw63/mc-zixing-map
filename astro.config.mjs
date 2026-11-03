// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://mc-zixing-map-site.pages.dev',
  integrations: [
    starlight({
      title: '紫星服务器',
      description: '紫星服务器玩家手册：入服指南、设施目录、假人目录、交通与服规',
      defaultLocale: 'root',
      locales: {
        root: { label: '简体中文', lang: 'zh-CN' },
      },
      customCss: ['./src/styles/theme.css'],
      // 文档挂在 /docs 下，首页留给 public/index.html（地图站）
      sidebar: [
        {
          label: '开始',
          items: [
            { label: '文档首页', slug: 'docs' },
            { label: '入服指南', slug: 'docs/join' },
            { label: '服规', slug: 'docs/rules' },
          ],
        },
        {
          label: '手册',
          items: [
            { label: '设施目录', slug: 'docs/facilities' },
            { label: '假人目录', slug: 'docs/bots' },
            { label: '交通', slug: 'docs/transport' },
          ],
        },
        {
          label: '给维护者',
          items: [{ label: '怎么改文档', slug: 'docs/contributing' }],
        },
      ],
      social: [
        {
          icon: 'github',
          label: 'GitHub 仓库',
          href: 'https://github.com/czw63/mc-zixing-map',
        },
      ],
      pagination: true,
      lastUpdated: true,
      // 首页是深色的，文档默认也走深色，用户仍可在右上角切换
      head: [
        {
          tag: 'script',
          content:
            "try{if(!localStorage.getItem('starlight-theme'))localStorage.setItem('starlight-theme','dark')}catch(e){}",
        },
      ],
    }),
  ],
});
