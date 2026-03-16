import 'package:flutter/material.dart';

/// 모바일 퍼스트 AI 교육 블로그 랜딩
/// - 햄버거 메뉴(Drawer)로 카테고리
/// - Hero 검색창 + 인스타그램 스타일 무한 스크롤 피드
void main() {
  runApp(const MaterialApp(
    title: 'AI 강의 자료실',
    debugShowCheckedModeBanner: false,
    home: LandingPage(),
  ));
}

/// 피드 한 칸 데이터
class FeedItem {
  const FeedItem({
    required this.title,
    required this.tag,
    required this.description,
    required this.thumbnailColor,
  });
  final String title;
  final String tag;
  final String description;
  final Color thumbnailColor;
}

/// 카테고리 Drawer 항목
class _CategoryItem {
  const _CategoryItem(this.icon, this.label);
  final IconData icon;
  final String label;
}

class LandingPage extends StatefulWidget {
  const LandingPage({super.key});

  @override
  State<LandingPage> createState() => _LandingPageState();
}

class _LandingPageState extends State<LandingPage> {
  static const _containerMaxWidth = 500.0;
  static const _backgroundColor = Color(0xFFF8F9FA);
  static const _pageSize = 10;

  final List<FeedItem> _feedItems = [];
  final ScrollController _scrollController = ScrollController();
  bool _isLoadingMore = false;
  bool _hasMore = true; // 실제 API에서는 서버가 더 있는지 반환
  int _page = 0;
  int _footerSelectedIndex = 0; // 푸터 선택 인덱스 (다른 기능 연동용)

  static const _categories = [
    _CategoryItem(Icons.memory, 'AI/ML'),
    _CategoryItem(Icons.settings, '환경설정'),
    _CategoryItem(Icons.terminal, 'FastAPI'),
    _CategoryItem(Icons.smartphone, 'Flutter'),
    _CategoryItem(Icons.account_tree_outlined, '데이터 흐름도'),
  ];

  /// 무한 스크롤용 더미 데이터 생성 (실제로는 API 호출로 교체)
  static final List<FeedItem> _mockPool = [
    const FeedItem(title: '개발환경 설정 한 번에', tag: '#환경설정', description: 'Python, CUDA, 가상환경부터 IDE까지', thumbnailColor: Color(0xFFE9D5FF)),
    const FeedItem(title: 'AI 입문 가이드', tag: '#AI입문', description: '머신러닝·딥러닝 기초와 실습', thumbnailColor: Color(0xFFFED7AA)),
    const FeedItem(title: 'FastAPI 데이터 흐름', tag: '#FastAPI', description: 'API 설계와 요청 흐름도', thumbnailColor: Color(0xFFA7F3D0)),
    const FeedItem(title: 'PyTorch 실습', tag: '#PyTorch', description: '텐서, autograd, 모델 학습', thumbnailColor: Color(0xFFBFDBFE)),
    const FeedItem(title: 'Flutter 레이아웃', tag: '#Flutter', description: '위젯과 반응형 UI', thumbnailColor: Color(0xFFFBCFE8)),
    const FeedItem(title: 'Docker 환경', tag: '#환경설정', description: '컨테이너로 재현 가능한 환경', thumbnailColor: Color(0xFFD1FAE5)),
    const FeedItem(title: 'RAG 파이프라인', tag: '#AI/ML', description: '검색 기반 생성 요약', thumbnailColor: Color(0xFFE0E7FF)),
    const FeedItem(title: 'REST API 설계', tag: '#FastAPI', description: '엔드포인트와 스키마', thumbnailColor: Color(0xFFFFE4E6)),
    const FeedItem(title: 'Mermaid 다이어그램', tag: '#ETL', description: '흐름도·시퀀스 다이어그램', thumbnailColor: Color(0xFFFEF3C7)),
    const FeedItem(title: 'Git 브랜치 전략', tag: '#환경설정', description: 'main/develop 워크플로우', thumbnailColor: Color(0xFFE5E7EB)),
  ];

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_onScroll);
    _loadMore();
  }

  @override
  void dispose() {
    _scrollController.removeListener(_onScroll);
    _scrollController.dispose();
    super.dispose();
  }

  void _onScroll() {
    if (!_hasMore || _isLoadingMore) return;
    final pos = _scrollController.position;
    if (pos.pixels >= pos.maxScrollExtent - 200) _loadMore();
  }

  Future<void> _loadMore() async {
    if (_isLoadingMore || !_hasMore) return;
    setState(() => _isLoadingMore = true);

    // 네트워크 지연 시뮬레이션
    await Future.delayed(const Duration(milliseconds: 400));

    final start = _page * _pageSize;
    final end = (start + _pageSize).clamp(0, _mockPool.length);
    for (var i = start; i < end; i++) {
      _feedItems.add(_mockPool[i % _mockPool.length]);
    }
    _page++;
    // mock: 계속 반복 로드. 실제 API에서는 응답의 hasMore 사용

    if (mounted) {
      setState(() => _isLoadingMore = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: _backgroundColor,
      appBar: AppBar(
        title: const Text('AI 강의 자료실', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
        centerTitle: true,
        backgroundColor: Colors.white,
        foregroundColor: Colors.grey[800],
        elevation: 0,
        scrolledUnderElevation: 1,
      ),
      drawer: _buildDrawer(context),
      bottomNavigationBar: _buildFixedFooter(context),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: _containerMaxWidth),
          child: Container(
            color: Colors.white,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                _buildHero(context),
                Expanded(
                  child: ListView.builder(
                    controller: _scrollController,
                    physics: const ClampingScrollPhysics(),
                    padding: const EdgeInsets.fromLTRB(16, 0, 16, 24), // 푸터는 Scaffold가 처리
                    itemCount: _feedItems.length + (_isLoadingMore ? 1 : 0),
                    itemBuilder: (context, index) {
                      if (index >= _feedItems.length) {
                        return const Padding(
                          padding: EdgeInsets.symmetric(vertical: 16),
                          child: Center(
                            child: SizedBox(
                              width: 24,
                              height: 24,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            ),
                          ),
                        );
                      }
                      return _FeedCard(item: _feedItems[index]);
                    },
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  /// 인스타/DM 스타일 고정 푸터 (버튼 4개, 다른 기능 연동용)
  Widget _buildFixedFooter(BuildContext context) {
    const items = [
      (Icons.home_outlined, Icons.home, '홈'),
      (Icons.search_outlined, Icons.search, '검색'),
      (Icons.add_circle_outline, Icons.add_circle, '작성'),
      (Icons.person_outline, Icons.person, '마이'),
    ];
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.06),
            blurRadius: 8,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: SafeArea(
        top: false,
        child: SizedBox(
          height: 56,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: List.generate(4, (index) {
              final (outlined, filled) = (items[index].$1, items[index].$2);
              final label = items[index].$3;
              final selected = _footerSelectedIndex == index;
              return Expanded(
                child: Material(
                  color: Colors.transparent,
                  child: InkWell(
                    onTap: () {
                      setState(() => _footerSelectedIndex = index);
                      // TODO: index별 기능 연동 (탭 화면 이동, 검색, 글쓰기, 마이페이지 등)
                    },
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          selected ? filled : outlined,
                          size: 26,
                          color: selected ? Colors.grey[800] : Colors.grey[600],
                        ),
                        const SizedBox(height: 4),
                        Text(
                          label,
                          style: TextStyle(
                            fontSize: 11,
                            color: selected ? Colors.grey[800] : Colors.grey[600],
                            fontWeight: selected ? FontWeight.w600 : FontWeight.w500,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              );
            }),
          ),
        ),
      ),
    );
  }

  Drawer _buildDrawer(BuildContext context) {
    return Drawer(
      child: SafeArea(
        child: ListView(
          padding: const EdgeInsets.symmetric(vertical: 8),
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(24, 24, 24, 16),
              child: Row(
                children: [
                  Icon(Icons.auto_awesome, color: Colors.grey[700]),
                  const SizedBox(width: 12),
                  Text(
                    '카테고리',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w600,
                      color: Colors.grey[800],
                    ),
                  ),
                ],
              ),
            ),
            const Divider(height: 1),
            ..._categories.map((c) => ListTile(
                  leading: Icon(c.icon, color: Colors.grey[600], size: 22),
                  title: Text(
                    c.label,
                    style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
                  ),
                  onTap: () {
                    Navigator.pop(context);
                    // TODO: 카테고리별 필터/화면 이동
                  },
                )),
          ],
        ),
      ),
    );
  }

  Widget _buildHero(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(20, 16, 20, 20),
      child: Column(
        children: [
          Text(
            '무엇을 도와드릴까요?',
            style: TextStyle(fontSize: 14, color: Colors.grey[600]),
          ),
          const SizedBox(height: 12),
          TextField(
            decoration: InputDecoration(
              hintText: '키워드 또는 태그로 검색...',
              hintStyle: TextStyle(color: Colors.grey[400], fontSize: 16),
              prefixIcon: Icon(Icons.search, color: Colors.grey[400], size: 22),
              filled: true,
              fillColor: Colors.grey[50],
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(24),
                borderSide: BorderSide(color: Colors.grey[200]!),
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(24),
                borderSide: BorderSide(color: Colors.grey[200]!),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(24),
                borderSide: BorderSide(color: Colors.grey[300]!, width: 1.5),
              ),
              contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
            ),
          ),
        ],
      ),
    );
  }
}

class _FeedCard extends StatelessWidget {
  const _FeedCard({required this.item});
  final FeedItem item;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Material(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        elevation: 1,
        shadowColor: Colors.black12,
        child: InkWell(
          onTap: () {},
          borderRadius: BorderRadius.circular(12),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 96,
                  height: 80,
                  decoration: BoxDecoration(
                    color: item.thumbnailColor,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(Icons.menu_book_outlined, size: 32, color: Colors.grey[500]),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        item.tag,
                        style: TextStyle(fontSize: 12, color: Colors.grey[500]),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        item.title,
                        style: const TextStyle(
                          fontSize: 15,
                          fontWeight: FontWeight.w600,
                          color: Colors.black87,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      Text(
                        item.description,
                        style: TextStyle(fontSize: 12, color: Colors.grey[500]),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
