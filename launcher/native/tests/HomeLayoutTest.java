import ua.empirecraft.launcherclient.HomeLayout;

public class HomeLayoutTest {
    private static void require(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }
    public static void main(String[] args) {
        int[][] sizes = {{320,240},{427,240},{640,360},{960,540},{1280,720},{1920,1080},{1067,300},{320,600}};
        for (int[] size : sizes) {
            var l = HomeLayout.of(size[0], size[1]);
            String context = size[0]+"x"+size[1];
            require(l.buttonX() >= 0 && l.buttonX()+l.buttonWidth() < l.stageLeft(), context+" navigation overlaps character stage");
            require(l.buttonY(0) >= l.margin()+70, context+" navigation overlaps heading");
            require(l.buttonY(2)+l.buttonHeight() < size[1]-l.margin(), context+" navigation clips bottom");
            require(l.feetY()-l.scale()*2.2 >= 0, context+" head clips top");
            require(l.characterX()-l.scale()*.65 >= l.stageLeft(), context+" model overlaps navigation");
            require(l.characterX()+l.scale()*.65 <= l.stageRight(), context+" model clips right");
            require(l.feetY() < l.appearanceY()-22, context+" model overlaps appearance controls");
            require(l.characterX()-l.appearanceWidth()-3 >= l.stageLeft(), context+" skin button clips left");
            require(l.characterX()+l.appearanceWidth()+3 <= l.stageRight(), context+" cape button clips right");
            require(l.appearanceY()+22 <= size[1]-8, context+" appearance controls clip bottom");
            require(l.onCharacter(l.characterX(), l.feetY()-l.scale()), context+" drag misses torso");
            require(!l.onCharacter(l.buttonX(), l.buttonY(0)), context+" navigation starts a model drag");
        }
        System.out.println("HOME_LAYOUT_PASS "+sizes.length+" sizes");
    }
}
