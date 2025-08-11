/**
 *@ClassName KakfaTest
 *@Description: TODO
 *@Date 2024/5/16 15:21
 **/

@RestController
public class KakfaTest {


	@RequestMapping("kafkatest")
	public void test() {

		try {
			String topicName = "kafka-test-1";
			KafkaUtil.createTopic(topicName, 1, (short) 1);//创建topic
			KafkaUtil.updateTopicRetention(topicName, String.valueOf(1000000));//更新topic的过期时间

			Set<String> strings = KafkaUtil.listTopic();//查出所有topic
			System.out.println("所有topic:" + strings);

			boolean b = KafkaUtil.existTopic(topicName);//查询topic是否存在
			System.out.println("topic-是否存在：" + b);


			String listenerID = "kafka-test-listener-1";

			//创建监听容器
			KafkaUtil.registerListenerContainer
					(listenerID, "test-consumer-group", new KakfaTest(), KakfaTest.class.getDeclaredMethod("consumerMessage", List.class), topicName);

			boolean b1 = KafkaUtil.existListenerContainer(listenerID);//查询监听容器是否存在
			System.out.println("容器-是否存在：" + b1);

			boolean normalStateListenerContainer = KafkaUtil.isNormalStateListenerContainer(listenerID);//查询监听容器是否为正常状态
			System.out.println("容器-状态：" + normalStateListenerContainer);

			KafkaUtil.pauseListenerContainer(listenerID);//暂停监听容器的监听状态
			boolean pauseStateListenerContainer = KafkaUtil.getPauseStateListenerContainer(listenerID);//查询监听容器的监听状态
			System.out.println("容器-监听状态：" + !pauseStateListenerContainer);


			KafkaUtil.stopListenerContainer(listenerID);//暂停监听容器的监听状态
			boolean runningStateListenerContainer = KafkaUtil.getRunningStateListenerContainer(listenerID);//查询监听容器的监听状态
			System.out.println("容器-运行状态：" + runningStateListenerContainer);


			boolean normalStateListenerContainer2 = KafkaUtil.isNormalStateListenerContainer(listenerID);//查询监听容器是否为正常状态
			System.out.println("容器-状态：" + normalStateListenerContainer2);


			boolean b2 = KafkaUtil.setStateNormalListenerContainer(listenerID);//设置监听容器为正常状态
			boolean normalStateListenerContainer3 = KafkaUtil.isNormalStateListenerContainer(listenerID);//查询监听容器是否为正常状态
			System.out.println("容器-状态：" + normalStateListenerContainer3);


		} catch (Exception e) {
			throw new RuntimeException(e);
		}
	}


	@RequestMapping("del")
	public void deleteTopic() throws Exception {
		String topicName = "kafka-test-1";
		KafkaUtil.deleteTopic(topicName);//删除topic
	}


	@RequestMapping("send")
	public void sendMsg() throws Exception {
		String topicName = "kafka-test-1";
		KafkaUtil.sendMsg(topicName, "haha");
		boolean b = KafkaUtil.existTopic(topicName);//查询topic是否存在
		System.out.println("topic-是否存在：" + b);
	}


	/**
	 * @Title consumerMessage
	 * @Description TODO 消费监听处理消息的方法
	 * @param message 接受来自kakfa的参数
	 * @param ack 消息确认参数
	 * @return void
	 */
	public void consumerMessage(List<ConsumerRecord<String, Object>> message, Acknowledgment ack) {
		System.out.println("收到消息：" + message);
		//消息确认
		ack.acknowledge();

	}

